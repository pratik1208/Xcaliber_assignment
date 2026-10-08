import json

from app.agent.graph import INSUFFICIENT, ask, build_graph


def fake_llm(answer_json):
    def complete(system, user, max_tokens=0):
        if "route questions" in system:
            return json.dumps({"intent": "longitudinal", "lab_name": "HbA1c", "search_text": "diabetes"})
        return json.dumps(answer_json)
    return build_graph(complete=complete)


def test_valid_answer_keeps_only_real_evidence():
    g = fake_llm({"kind": "answer", "answer": "HbA1c fell from 8.2% to 7.1%.",
                  "evidence_ids": ["obs:O001", "obs:O010", "obs:FAKE", "obs:O101"]})
    r = ask("P001", "How has diabetes progressed?", g)
    assert r["kind"] == "answer"
    assert [e["record_id"] for e in r["evidence"]] == ["obs:O001", "obs:O010"]


def test_answer_without_valid_evidence_becomes_insufficient():
    g = fake_llm({"kind": "answer", "answer": "Made up.", "evidence_ids": ["obs:NOPE"]})
    r = ask("P001", "Smoking history?", g)
    assert r["answer"] == INSUFFICIENT and r["evidence"] == []


def test_refusal_passes_through():
    g = fake_llm({"kind": "refusal", "answer": "I can only summarise the record.", "evidence_ids": ["med:M001"]})
    assert ask("P001", "Increase metformin?", g)["kind"] == "refusal"


def test_other_patient_evidence_rejected():
    g = fake_llm({"kind": "answer", "answer": "x", "evidence_ids": ["obs:O101"]})  # P002 record
    assert ask("P001", "q", g)["answer"] == INSUFFICIENT


def test_llm_garbage_is_insufficient():
    def complete(system, user, max_tokens=0):
        return "not json"
    assert ask("P001", "q", build_graph(complete=complete))["answer"] == INSUFFICIENT
