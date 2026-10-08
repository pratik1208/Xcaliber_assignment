const BASE = import.meta.env.VITE_API_URL || "/api";

async function request(path, options) {
  let res;
  try {
    res = await fetch(`${BASE}${path}`, options);
  } catch {
    throw new Error("Cannot reach the API. Is the backend running on port 8000?");
  }
  if (!res.ok) {
    let detail = res.statusText;
    try { detail = (await res.json()).detail || detail; } catch { /* non-JSON error body */ }
    throw new Error(detail);
  }
  return res.json();
}

export const getPatients = () => request("/patients");
export const getSummary = (id) => request(`/patients/${id}/summary`);
export const askQuestion = (id, question) =>
  request(`/patients/${id}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
