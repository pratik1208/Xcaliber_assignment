export default function PatientSummary({ summary: s }) {
  const p = s.patient;
  return (
    <section className="card">
      <h2>{p.name} <span className="muted">· {p.sex} · DOB {p.birth_date}</span></h2>
      <div className="grid3">
        <div>
          <h3>Active conditions</h3>
          <ul>{s.conditions.map((c) => <li key={c.record_id}>{c.display} <span className="muted">(since {c.onset_date})</span></li>)}</ul>
          <h3>Current medications</h3>
          <ul>{s.medications.map((m) => <li key={m.record_id}>{m.display} — {m.dose}</li>)}</ul>
        </div>
        <div>
          <h3>Recent encounters</h3>
          <ul>{s.encounters.map((e) => <li key={e.record_id}>{e.date} · {e.type} · {e.reason}</li>)}</ul>
          <h3>Recent procedures</h3>
          <ul>{s.procedures.length ? s.procedures.map((x) => <li key={x.record_id}>{x.date} · {x.display}</li>) : <li className="muted">None recorded</li>}</ul>
        </div>
        <div>
          <h3>Latest observations</h3>
          <ul>{s.observations.map((o) => <li key={o.record_id}>{o.name}: <b>{o.value} {o.unit}</b> <span className="muted">({o.date})</span></li>)}</ul>
        </div>
      </div>
    </section>
  );
}
