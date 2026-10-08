# Patient 360 — Demo Implementation Plan

Goal: a working demo of the stack in `plan.md`, kept as small as possible. Demo-first means: synthetic data, one command to start, a polished happy path for the P001 diabetes story, no auth, no production hardening.

## 1. Architecture (one picture)

```
Streamlit (UI)  ──HTTP──►  FastAPI  ──►  LangGraph agent
 patient picker             /patients            │
 Patient 360 panel          /patients/{id}/summary ├─► SQL tools ──► PostgreSQL (simplified FHIR tables)
 chat + evidence panel      /patients/{id}/ask     └─► note search ─► ChromaDB (BGE embeddings of notes)
```

Docker Compose runs 3 containers: `postgres`, `api` (FastAPI + Chroma embedded, persisted to a volume), `ui` (Streamlit).

## 2. Repo layout

```
data/seed/            generated synthetic JSON (FHIR-lite) + notes/*.txt
scripts/generate_data.py   builds the seed data (deterministic)
scripts/ingest.py          Pandas: seed -> Postgres tables, notes -> Chroma
app/api/main.py            FastAPI routes
app/agent/graph.py         LangGraph graph
app/agent/tools.py         SQL + note-search tools (all scoped to patient_id)
app/db.py                  SQLAlchemy models/connection
app/ui/streamlit_app.py    UI
tests/                     tool tests + eval questions
docker-compose.yml, Dockerfile, .env.example
```

## 3. Data (synthetic, demo-shaped)

- Simplified FHIR tables: `patient, encounter, condition, medication_request, observation, procedure`, each with `id`, `patient_id`, `date`, and a `encounter_id` link where relevant.
- `notes` stored as text files, one per encounter, chunked and embedded into Chroma with metadata `{patient_id, encounter_id, date, note_id}`.
- **P001 (hero patient):** type 2 diabetes, HbA1c 8.2 → 7.1 over 12 months, one ER visit for hyperglycemia then outpatient follow-ups, metformin continuous, plus hypertension and a few other labs/procedures for the summary panel.
- **P002:** a different profile (e.g. CKD + a stopped medication), used to show patient switching, an unanswerable question, and that data does not leak between patients.
- Notes include one unresolved follow-up and one documented concern, so the "unresolved issues" and "concerns" questions have real answers.

## 4. Agent (LangGraph, deliberately tiny)

Nodes:
1. **route** — LLM classifies the question: `summary | structured | notes | longitudinal` (longitudinal = both structured + notes).
2. **retrieve** — runs the tools the route needs:
   - `get_encounters(n, since)`, `get_conditions(active_only)`, `get_medications(active_only)`, `get_observations(name, since)`, `get_procedures(since)` — SQL via SQLAlchemy.
   - `search_notes(query, k)` — Chroma query filtered by `patient_id`.
   Every returned row carries a `record_id` (e.g. `obs:123`, `note:7`).
3. **answer** — LLM gets only the retrieved records and returns JSON `{answer, evidence_ids[], sufficient: bool}`. System prompt rules: use only the supplied records; if not supported, say "Insufficient evidence in the available records."; no diagnosis, no treatment or medication advice.
4. **validate** (plain code, no LLM) — drop any `evidence_id` not in the retrieved set; if no valid evidence remains or `sufficient=false`, replace the answer with the insufficient-evidence message.

The patient id is injected by the API into every tool call, never chosen by the LLM.

## 5. API (FastAPI)

- `GET /patients` — list for the dropdown.
- `GET /patients/{id}/summary` — Patient 360 (active conditions, current meds, last 3 encounters, key labs, recent procedures). Plain SQL, no LLM, so it is instant and reliable in the demo.
- `POST /patients/{id}/ask` `{question}` → `{answer, evidence: [{id, type, date, text}]}`.

## 6. UI (Streamlit)

- Sidebar: patient dropdown + a few sample-question buttons (the four questions from `plan.md` plus the diabetes progression one).
- Main: Patient 360 panel at the top; below it a chat. Under each answer, an "Evidence" expander lists the cited records (date, type, text; notes shown as quoted excerpts).
- For lab questions, a small HbA1c line chart from the evidence (`st.line_chart`).
- Always-visible caption: "Information retrieval only — not clinical advice."

## 7. Build order (each step is demoable)

1. **Data + DB:** `generate_data.py`, Postgres schema, `ingest.py`. Check with SQL that P001 shows 8.2 → 7.1.
2. **API summary endpoint** + **Streamlit shell** with the patient picker and Patient 360 panel. (Demo-able with no LLM.)
3. **Tools + Chroma note ingest/search**, with unit tests for each tool.
4. **LangGraph agent** + `/ask` endpoint + validate node.
5. **Chat UI + evidence panel + chart.**
6. **Docker Compose** (one `docker compose up`) and a README with the demo script.
7. **Eval pass:** run the demo questions (below), tune prompts.

## 8. Demo script / acceptance checks

| Question (patient) | Expected |
|---|---|
| Summary load (P001) | conditions, meds, encounters, labs, procedures shown |
| "How has this patient's diabetes progressed over the last year?" (P001) | improved; HbA1c 8.2% → 7.1%; ER visit; metformin continued; evidence lists the labs, encounters, meds and notes |
| "What medications is the patient currently taking?" | matches active medication rows |
| "What happened during the last three encounters?" | three encounters with dates |
| "What concerns were documented during recent visits?" | cites note excerpts |
| "Are there any unresolved follow-ups?" | cites the note with the pending follow-up |
| Unanswerable question, e.g. "What is the patient's smoking history?" (not in data) | "Insufficient evidence in the available records." |
| "Should we increase the metformin dose?" | declines to give treatment advice; offers the relevant records only |
| Switch to P002 and repeat | no P001 data appears |

## 9. Deliberately cut for the demo

Auth/users, real FHIR parsing, reranking, streaming, conversation memory beyond the current question, background jobs, CI/CD, observability. Embeddings run locally (BGE small) so the only external dependency is the LLM API key (`.env`).

## 10. Risks and defaults

- **LLM provider:** default to Claude via the Anthropic SDK; the provider sits behind one `llm.py` function so OpenAI can be swapped in.
- **Model download time** for BGE on first run: pre-download in the Docker image build.
- **Number accuracy:** trend values come straight from SQL rows in the evidence; the prompt tells the LLM to quote values, never compute new ones beyond the first/last difference.
