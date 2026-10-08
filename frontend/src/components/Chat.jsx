import { useEffect, useRef, useState } from "react";
import { askQuestion } from "../api.js";
import Evidence from "./Evidence.jsx";

export default function Chat({ patientId, pending, onConsumed }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const endRef = useRef(null);
  const lastPending = useRef(null);

  async function send(question) {
    if (!question.trim() || busy) return;
    setMessages((m) => [...m, { role: "user", text: question }]);
    setInput("");
    setBusy(true);
    try {
      const r = await askQuestion(patientId, question);
      setMessages((m) => [...m, { role: "assistant", text: r.answer, evidence: r.evidence }]);
    } catch (e) {
      setMessages((m) => [...m, { role: "assistant", text: `⚠️ ${e.message}`, error: true }]);
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    if (pending && pending !== lastPending.current) {
      lastPending.current = pending;
      onConsumed?.(); // a sample question is asked once, for the patient it was clicked on
      send(pending.q);
    }
  }, [pending]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, busy]);

  return (
    <section className="chat">
      <div className="messages">
        {messages.length === 0 && <p className="muted">Ask a question about this patient, or pick a sample question.</p>}
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role} ${m.error ? "err" : ""}`}>
            <div>{m.text}</div>
            {m.role === "assistant" && <Evidence evidence={m.evidence} />}
          </div>
        ))}
        {busy && <div className="msg assistant muted">Reviewing the record…</div>}
        <div ref={endRef} />
      </div>
      <form className="composer" onSubmit={(e) => { e.preventDefault(); send(input); }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask about this patient…" disabled={busy} />
        <button type="submit" disabled={busy || !input.trim()}>Send</button>
      </form>
    </section>
  );
}
