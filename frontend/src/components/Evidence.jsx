import { useState } from "react";
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

function Row({ e }) {
  const id = <code>{e.record_id}</code>;
  switch (e.type) {
    case "observation": return <>{id} <b>{e.date} · Lab</b> — {e.name} {e.value} {e.unit}</>;
    case "medication": return <>{id} <b>{e.start_date} · Medication</b> — {e.display} {e.dose} ({e.status})</>;
    case "encounter": return <>{id} <b>{e.date} · Encounter ({e.type})</b> — {e.reason}</>;
    case "condition": return <>{id} <b>{e.onset_date} · Diagnosis</b> — {e.display} ({e.status})</>;
    case "procedure": return <>{id} <b>{e.date} · Procedure</b> — {e.display}</>;
    default: return <>{id} <b>{e.date} · Clinical note</b> ({e.encounter_id})<blockquote>{e.text}</blockquote></>;
  }
}

export default function Evidence({ evidence }) {
  const [open, setOpen] = useState(false);
  if (!evidence?.length) return null;
  const labs = evidence.filter((e) => e.type === "observation");
  const names = [...new Set(labs.map((l) => l.name))].filter((n) => labs.filter((l) => l.name === n).length > 1);
  return (
    <div className="evidence">
      <button className="link" onClick={() => setOpen(!open)}>
        {open ? "▾" : "▸"} Evidence ({evidence.length} records)
      </button>
      {open && (
        <div>
          {names.map((n) => {
            const pts = labs.filter((l) => l.name === n).map((l) => ({ date: l.date, value: l.value }));
            return (
              <div key={n} className="chart">
                <b>{n} trend</b>
                <ResponsiveContainer width="100%" height={180}>
                  <LineChart data={pts}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" fontSize={11} />
                    <YAxis domain={["auto", "auto"]} fontSize={11} />
                    <Tooltip />
                    <Line type="monotone" dataKey="value" stroke="#2563eb" strokeWidth={2} dot />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            );
          })}
          <ul className="evlist">{evidence.map((e) => <li key={e.record_id}><Row e={e} /></li>)}</ul>
        </div>
      )}
    </div>
  );
}
