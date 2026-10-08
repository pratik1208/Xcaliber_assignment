import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import PatientPicker from "./PatientPicker.jsx";

const patients = [
  { id: "P001", name: "Maria Alvarez" },
  { id: "P002", name: "James Whitfield" },
  { id: "P003", name: "Olivia Smith" },
  { id: "P004", name: "Mario Lopez" },
];

function Harness({ onPick }) {
  const [v, setV] = useState("P001");
  return <PatientPicker patients={patients} value={v} onChange={(id) => { setV(id); onPick?.(id); }} />;
}

const box = () => screen.getByRole("combobox");
const names = () => screen.queryAllByRole("option").map((o) => o.textContent);

test("shows the selected patient and lists everyone on focus", async () => {
  render(<Harness />);
  expect(box().value).toBe("P001 — Maria Alvarez");
  await userEvent.click(box());
  expect(names()).toHaveLength(4);
});

test("filters by name, case-insensitively", async () => {
  render(<Harness />);
  await userEvent.click(box());
  await userEvent.keyboard("mari");
  expect(names().map((n) => n.replace(/^P\d+/, "").trim())).toEqual(["Maria Alvarez", "Mario Lopez"]);
});

test("filters by patient id", async () => {
  render(<Harness />);
  await userEvent.click(box());
  await userEvent.keyboard("p003");
  expect(names()).toHaveLength(1);
  expect(names()[0]).toContain("Olivia Smith");
});

test("shows an empty state when nothing matches", async () => {
  render(<Harness />);
  await userEvent.click(box());
  await userEvent.keyboard("zzz");
  expect(screen.getByText("No matching patients")).toBeTruthy();
});

test("clicking a result selects it and closes the list", async () => {
  const onPick = vi.fn();
  render(<Harness onPick={onPick} />);
  await userEvent.click(box());
  await userEvent.keyboard("whit");
  await userEvent.click(screen.getByRole("option"));
  expect(onPick).toHaveBeenCalledWith("P002");
  expect(box().value).toBe("P002 — James Whitfield");
  expect(screen.queryByRole("listbox")).toBeNull();
});

test("arrow keys + Enter select; Escape closes without changing", async () => {
  const onPick = vi.fn();
  render(<Harness onPick={onPick} />);
  await userEvent.click(box());
  await userEvent.keyboard("{ArrowDown}{ArrowDown}{Enter}");
  expect(onPick).toHaveBeenCalledWith("P003");

  await userEvent.click(box());
  await userEvent.keyboard("xyz{Escape}");
  expect(screen.queryByRole("listbox")).toBeNull();
  expect(box().value).toBe("P003 — Olivia Smith"); // reverts to the current patient
});
