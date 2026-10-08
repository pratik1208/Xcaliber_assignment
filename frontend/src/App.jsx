import { useEffect, useState } from "react";
import { getPatients, getSummary } from "./api.js";
import PatientSummary from "./components/PatientSummary.jsx";
import Chat from "./components/Chat.jsx";
import PatientPicker from "./components/PatientPicker.jsx";

// Hand-picked for the hero patient (Maria Alvarez, P001: diabetes + hypertension + hyperlipidemia).
const PATIENT_SAMPLES = {
  P001: [
    "How has this patient's diabetes progressed over the last year?",
    "How has the HbA1c changed over the last year?",
    "What happened during the emergency visit for hyperglycemia?",
    "What medications is the patient currently taking?",
    "How has the blood pressure changed over time?",
    "What did the physician document about foot numbness?",
    "Are there any unresolved follow-ups?",
    "Has the retinal eye exam been completed?",
    "What is the patient's smoking history?",
    "Should we increase the metformin dose?",
  ],
};

// Other patients: questions built from their active conditions.
const CONDITION_SAMPLES = [
  [/diabetes/i, ["How has this patient's diabetes progressed over the last year?", "How has the HbA1c changed over time?"]],
  [/hypertension/i, ["How has the blood pressure changed over time?"]],
  [/kidney/i, ["How has the kidney function (eGFR) changed over time?"]],
  [/lipid/i, ["How has the LDL cholesterol changed over time?"]],
  [/asthma/i, ["How has the lung function (FEV1) changed over time?"]],
  [/heart failure/i, ["How has the BNP changed over time?"]],
];

function buildSamples(summary) {
  if (PATIENT_SAMPLES[summary.patient.id]) return PATIENT_SAMPLES[summary.patient.id];
  const names = summary.conditions.map((c) => c.display).join(" | ");
  const specific = CONDITION_SAMPLES.filter(([re]) => re.test(names)).flatMap(([, qs]) => qs);
  return [
    ...specific.slice(0, 3),
    "What medications is the patient currently taking?",
    "What happened during the patient's last three encounters?",
    "What concerns were documented during recent visits?",
    "Are there any unresolved follow-ups?",
    "What is the patient's smoking history?",
    "Should we change this patient's medication dose?",
  ];
}

export default function App() {
  const [patients, setPatients] = useState([]);
  const [pid, setPid] = useState("");
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");
  const [pending, setPending] = useState(null);

  useEffect(() => {
    getPatients()
      .then((p) => { setPatients(p); setPid(p[0]?.id || ""); })
      .catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    if (!pid) return;
    let stale = false; // ignore a slow response for a patient we've already switched away from
    setSummary(null);
    setError("");
    getSummary(pid).then((s) => { if (!stale) setSummary(s); }).catch((e) => { if (!stale) setError(e.message); });
    return () => { stale = true; };
  }, [pid]);

  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>🩺 Patient 360</h1>
        <label htmlFor="patient">Patient</label>
        <PatientPicker patients={patients} value={pid} onChange={setPid} />
        <h2>Sample questions</h2>
        {(summary ? buildSamples(summary) : []).map((q) => (
          <button key={q} className="sample" onClick={() => setPending({ q, n: Date.now() })}>{q}</button>
        ))}
      </aside>
      <main className="main">
        <p className="disclaimer">Information retrieval only — not clinical advice. Verify answers against the cited records.</p>
        {error && <div className="error">{error}</div>}
        {summary && <PatientSummary summary={summary} />}
        {pid && <Chat key={pid} patientId={pid} pending={pending} onConsumed={() => setPending(null)} />}
      </main>
    </div>
  );
}
