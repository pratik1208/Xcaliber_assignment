import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App.jsx";

const patients = [{ id: "P001", name: "Maria Alvarez" }, { id: "P002", name: "James Whitfield" }];
const summary = (id, name) => ({
  patient: { id, name, sex: "x", birth_date: "1970-01-01" },
  conditions: [{ record_id: `c:${id}`, display: "Type 2 diabetes mellitus", onset_date: "2020-01-01" }],
  medications: [], encounters: [], observations: [], procedures: [],
});

beforeEach(() => {
  window.HTMLElement.prototype.scrollIntoView = () => {};
  global.fetch = vi.fn(async (url, opts) => {
    const ok = (body) => ({ ok: true, json: async () => body });
    if (url.endsWith("/patients")) return ok(patients);
    if (url.endsWith("/P001/summary")) return ok(summary("P001", "Maria Alvarez"));
    if (url.endsWith("/P002/summary")) return ok(summary("P002", "James Whitfield"));
    if (url.includes("/ask")) return ok({ answer: `answer for ${url.split("/")[3]}`, kind: "answer", evidence: [] });
    throw new Error("unexpected " + url);
  });
});

test("switching patient clears the chat and does not re-ask the old sample question", async () => {
  render(<App />);
  await screen.findByText(/Maria Alvarez/, { selector: "h2" });

  await userEvent.click(screen.getAllByRole("button").find((b) => b.className === "sample"));
  await screen.findByText("answer for P001");

  await userEvent.click(screen.getByRole("combobox"));
  await userEvent.click(await screen.findByRole("option", { name: /James/ }));

  await screen.findByText(/James Whitfield/, { selector: "h2" });
  await waitFor(() => expect(screen.queryByText("answer for P001")).toBeNull());
  expect(screen.getByText(/Ask a question about this patient/)).toBeTruthy();
  const asks = global.fetch.mock.calls.filter(([u]) => u.includes("/ask"));
  expect(asks).toHaveLength(1); // only the original P001 question; nothing re-fired for P002
});
