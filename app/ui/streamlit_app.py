import os

import pandas as pd
import requests
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")
SAMPLES = [
    "How has this patient's diabetes progressed over the last year?",
    "What medications is the patient currently taking?",
    "What happened during the patient's last three encounters?",
    "What concerns were documented during recent visits?",
    "Are there any unresolved follow-ups?",
    "What is the patient's smoking history?",
    "Should we increase the metformin dose?",
]

st.set_page_config(page_title="Patient 360", page_icon="🩺", layout="wide")
st.title("🩺 Patient 360 — Clinical Intelligence Agent")
st.caption("Information retrieval only — not clinical advice. Verify answers against the cited records.")


@st.cache_data(ttl=30)
def get(path):
    r = requests.get(f"{API}{path}", timeout=30)
    r.raise_for_status()
    return r.json()


patients = get("/patients")
labels = {f"{p['id']} — {p['name']}": p["id"] for p in patients}
choice = st.sidebar.selectbox("Patient", list(labels))
pid = labels[choice]
if st.session_state.get("pid") != pid:
    st.session_state.update(pid=pid, chat=[], pending=None)

st.sidebar.markdown("**Sample questions**")
for q in SAMPLES:
    if st.sidebar.button(q, use_container_width=True):
        st.session_state.pending = q

# ---- Patient 360 summary (plain SQL, no LLM) ----
s = get(f"/patients/{pid}/summary")
p = s["patient"]
st.subheader(f"{p['name']} · {p['sex']} · DOB {p['birth_date']}")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**Active conditions**")
    for c in s["conditions"]:
        st.write(f"• {c['display']} (since {c['onset_date']})")
    st.markdown("**Current medications**")
    for m in s["medications"]:
        st.write(f"• {m['display']} — {m['dose']}")
with c2:
    st.markdown("**Recent encounters**")
    for e in s["encounters"]:
        st.write(f"• {e['date']} · {e['type']} · {e['reason']}")
    st.markdown("**Recent procedures**")
    for pr in s["procedures"]:
        st.write(f"• {pr['date']} · {pr['display']}")
with c3:
    st.markdown("**Latest observations**")
    for o in s["observations"]:
        st.write(f"• {o['name']}: {o['value']} {o['unit']} ({o['date']})")

st.divider()


def render_evidence(ev):
    if not ev:
        return
    with st.expander(f"Evidence ({len(ev)} records)"):
        labs = [e for e in ev if e["type"] == "observation"]
        for name in sorted({e["name"] for e in labs}):
            pts = [e for e in labs if e["name"] == name]
            if len(pts) > 1:
                st.markdown(f"**{name} trend**")
                st.line_chart(pd.DataFrame({"date": [x["date"] for x in pts], name: [x["value"] for x in pts]}).set_index("date"))
        for e in ev:
            t = e["type"]
            if t == "observation":
                line = f"**{e['date']} · Lab** — {e['name']} {e['value']} {e['unit']}"
            elif t == "medication":
                line = f"**{e['start_date']} · Medication** — {e['display']} {e['dose']} ({e['status']})"
            elif t == "encounter":
                line = f"**{e['date']} · Encounter ({e['type']})** — {e['reason']}"
            elif t == "condition":
                line = f"**{e['onset_date']} · Diagnosis** — {e['display']} ({e['status']})"
            elif t == "procedure":
                line = f"**{e['date']} · Procedure** — {e['display']}"
            else:
                line = f"**{e['date']} · Clinical note** ({e['encounter_id']})\n\n> {e['text']}"
            st.markdown(f"`{e['record_id']}` {line}")


for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            render_evidence(m.get("evidence"))

typed = st.chat_input("Ask about this patient…")
q = typed or st.session_state.pending
st.session_state.pending = None
if q:
    st.session_state.chat.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        with st.spinner("Reviewing the record…"):
            try:
                r = requests.post(f"{API}/patients/{pid}/ask", json={"question": q}, timeout=120)
                r.raise_for_status()
                data = r.json()
            except Exception as ex:
                data = {"answer": f"Error: {ex}", "evidence": []}
        st.write(data["answer"])
        render_evidence(data["evidence"])
    st.session_state.chat.append({"role": "assistant", "content": data["answer"], "evidence": data["evidence"]})
