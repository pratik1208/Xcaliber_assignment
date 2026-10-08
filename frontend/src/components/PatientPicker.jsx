import { useEffect, useMemo, useRef, useState } from "react";

const label = (p) => `${p.id} — ${p.name}`;

export default function PatientPicker({ patients, value, onChange }) {
  const selected = patients.find((p) => p.id === value);
  const [text, setText] = useState("");
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const box = useRef(null);

  // Show the selected patient in the box whenever it isn't being edited.
  useEffect(() => { if (!open) setText(selected ? label(selected) : ""); }, [selected, open]);

  const matches = useMemo(() => {
    const q = text.trim().toLowerCase();
    if (!q || (selected && text === label(selected))) return patients;
    return patients.filter((p) => label(p).toLowerCase().includes(q));
  }, [patients, text, selected]);

  useEffect(() => { setActive(0); }, [text]);

  useEffect(() => {
    const close = (e) => { if (box.current && !box.current.contains(e.target)) setOpen(false); };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  function pick(p) {
    onChange(p.id);
    setOpen(false);
  }

  function onKeyDown(e) {
    if (e.key === "ArrowDown") { e.preventDefault(); setOpen(true); setActive((a) => Math.min(a + 1, matches.length - 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setActive((a) => Math.max(a - 1, 0)); }
    else if (e.key === "Enter" && open && matches[active]) { e.preventDefault(); pick(matches[active]); }
    else if (e.key === "Escape") { setOpen(false); }
  }

  return (
    <div className="picker" ref={box}>
      <input
        id="patient"
        type="search"
        autoComplete="off"
        placeholder="Search by name or ID…"
        value={text}
        onFocus={(e) => { setOpen(true); e.target.select(); }}
        onChange={(e) => { setText(e.target.value); setOpen(true); }}
        onKeyDown={onKeyDown}
        role="combobox"
        aria-expanded={open}
        aria-controls="patient-list"
      />
      {open && (
        <ul id="patient-list" className="picker-list" role="listbox">
          {matches.length === 0 && <li className="picker-empty">No matching patients</li>}
          {matches.map((p, i) => (
            <li
              key={p.id}
              role="option"
              aria-selected={p.id === value}
              className={`${i === active ? "active" : ""} ${p.id === value ? "current" : ""}`}
              onMouseEnter={() => setActive(i)}
              onMouseDown={(e) => { e.preventDefault(); pick(p); }}
            >
              <b>{p.id}</b> {p.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
