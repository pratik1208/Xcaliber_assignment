"""LangGraph agent: route -> retrieve -> answer -> validate.

The LLM never chooses the patient and never sees records outside the retrieved set.
`validate` is plain code: it removes evidence ids that were not retrieved and replaces
unsupported answers with the standard insufficient-evidence message."""
from typing import Callable, TypedDict

from langgraph.graph import END, StateGraph

from app.agent import llm as default_llm
from app.agent import tools

INSUFFICIENT = "Insufficient evidence in the available records."

ROUTE_SYSTEM = """You route questions about ONE patient's medical record. Reply with JSON only:
{"intent": "medications|labs|encounters|notes|longitudinal",
 "lab_name": "<lab/observation name such as HbA1c, or null>",
 "search_text": "<short phrase to search clinical notes for>"}
Use "longitudinal" for trends/progress/improvement questions, "labs" for lab values, "medications" for drug
questions, "encounters" for what happened at visits, "notes" for documented concerns/follow-ups."""

ANSWER_SYSTEM = f"""You are a clinical record retrieval assistant helping a physician review ONE patient's chart.
Use ONLY the records provided. Each record starts with its id in brackets, e.g. [obs:O010].
Rules:
- Be concise (3-6 sentences). Quote values and dates exactly as recorded; do not invent or estimate.
- Attribute each value to the exact date shown on its own record. When comparing visits, say a value was not recorded at a visit if no record exists for that date; never carry a value from another date.
- Describe trends only from the recorded values. Do not diagnose, recommend treatment or medication changes,
  or make clinical decisions. If asked for such advice, set "kind" to "refusal", say you can only summarise the
  record, and cite the relevant records.
- If the records do not contain enough to answer, set "kind" to "insufficient".
Reply with JSON only:
{{"kind": "answer|refusal|insufficient", "answer": "<text>", "evidence_ids": ["obs:O010", ...]}}
Cite only ids that appear in the records, and cite every record your answer relies on. If insufficient,
the answer text must be exactly: {INSUFFICIENT}"""


class State(TypedDict, total=False):
    patient_id: str
    question: str
    route: dict
    records: list
    result: dict

# Its purpose is to convert a retrieved medical record dictionary into a clean text format that can be sent to the LLM.
def fmt(r: dict) -> str:
    skip = {"id", "record_id", "type", "patient_id"}
    body = "; ".join(f"{k}={v}" for k, v in r.items() if k not in skip and v is not None)
    return f"[{r['record_id']}] ({r['type']}) {body}"


def build_graph(complete: Callable = None, parse: Callable = None):
    complete = complete or default_llm.complete
    parse = parse or default_llm.parse_json

    def route(s: State):
        try:
            r = parse(complete(ROUTE_SYSTEM, s["question"], 200))
        except ValueError:  # unparseable output -> default route; API errors propagate
            r = {}
        if r.get("intent") not in {"medications", "labs", "encounters", "notes", "longitudinal"}:
            r["intent"] = "longitudinal"
        return {"route": r}

    def retrieve(s: State):
        pid, r = s["patient_id"], s["route"]
        intent, lab, text = r["intent"], r.get("lab_name"), r.get("search_text") or s["question"]
        recs = []
        if intent == "medications":
            recs += tools.get_medications(pid) + tools.search_notes(pid, text, 3)
        elif intent == "labs":
            recs += tools.get_observations(pid, name=lab) + tools.get_encounters(pid)
        elif intent == "encounters":
            recs += tools.get_encounters(pid) + tools.get_all_notes(pid)
        elif intent == "notes":
            recs += tools.search_notes(pid, text, 5) + tools.get_encounters(pid)
        else:  # longitudinal: structured data across time + relevant notes
            recs += (tools.get_conditions(pid) + tools.get_medications(pid) + tools.get_observations(pid, name=lab)
                     + tools.get_encounters(pid) + tools.search_notes(pid, text, 5))
        seen, uniq = set(), []
        for x in recs:
            if x["record_id"] not in seen:
                seen.add(x["record_id"])
                uniq.append(x)
        return {"records": uniq}

    def answer(s: State):
        recs = s["records"]
        if not recs:
            return {"result": {"kind": "insufficient", "answer": INSUFFICIENT, "evidence_ids": []}}
        user = f"Question: {s['question']}\n\nPatient records:\n" + "\n".join(fmt(r) for r in recs)
        try:
            res = parse(complete(ANSWER_SYSTEM, user))
        except ValueError:  # unparseable output is treated as insufficient; API errors propagate
            res = {"kind": "insufficient", "answer": INSUFFICIENT, "evidence_ids": []}
        return {"result": res}

    def validate(s: State):
        res = s["result"]
        valid = {r["record_id"] for r in s["records"]}
        ids = [i for i in dict.fromkeys(res.get("evidence_ids") or []) if i in valid]
        kind = res.get("kind")
        if kind not in {"answer", "refusal"} or not str(res.get("answer", "")).strip() or (kind == "answer" and not ids):
            return {"result": {"kind": "insufficient", "answer": INSUFFICIENT, "evidence_ids": []}}
        return {"result": {"kind": kind, "answer": res["answer"].strip(), "evidence_ids": ids}}

    g = StateGraph(State)
    for name, fn in [("n_route", route), ("n_retrieve", retrieve), ("n_answer", answer), ("n_validate", validate)]:
        g.add_node(name, fn)
    g.set_entry_point("n_route")
    g.add_edge("n_route", "n_retrieve")
    g.add_edge("n_retrieve", "n_answer")
    g.add_edge("n_answer", "n_validate")
    g.add_edge("n_validate", END)
    return g.compile()


def ask(patient_id: str, question: str, graph=None) -> dict:
    graph = graph or _default()
    out = graph.invoke({"patient_id": patient_id, "question": question})
    res = out["result"]
    evidence = [r for r in (tools.get_record(i, patient_id) for i in res["evidence_ids"]) if r]
    return {"answer": res["answer"], "kind": res["kind"], "route": out["route"]["intent"], "evidence": evidence}


_graph = None


def _default():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
