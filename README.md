# Patient 360 — Clinical Intelligence Agent (demo)

Ask natural-language questions about a patient's record; get a concise answer plus the cited records.
**Backend:** FastAPI · LangGraph · OpenAI · PostgreSQL · ChromaDB (BGE) · Pandas. **Frontend:** React (Vite). Synthetic data only (120 patients).

    backend/    FastAPI app (app/), data generator + ingest (scripts/), seed data (data/), tests/
    frontend/   React single-page app (src/)

## Run locally
    # backend/.env needs OPENAI_API_KEY (copy backend/.env.example)
    ./run.sh          # API http://localhost:8000/docs · UI http://localhost:5173

Or by hand, in separate terminals:

    cd backend && uv venv --python 3.12 .venv && uv pip install -r requirements.txt
    createdb patient360
    .venv/bin/python scripts/generate_data.py && .venv/bin/python scripts/ingest.py
    .venv/bin/uvicorn app.api.main:app --port 8000

    cd frontend && npm install && npm run dev

Backend tests (offline, LLM faked): `cd backend && .venv/bin/python -m pytest tests`

## Run with Docker
    cp backend/.env.example backend/.env   # add OPENAI_API_KEY
    docker compose up --build              # UI http://localhost:3000 · API http://localhost:8000/docs

## Demo script
1. Pick **P001** → Patient 360 panel loads from SQL (no LLM).
2. "How has this patient's diabetes progressed over the last year?" → improved, HbA1c 8.2% → 7.1%, with chart + evidence.
3. "What concerns were documented during recent visits?" / "Are there any unresolved follow-ups?" → cites notes.
4. "What is the patient's smoking history?" → *Insufficient evidence in the available records.*
5. "Should we increase the metformin dose?" → declines advice, shows relevant records.
6. Switch patient (P002 or any of P003–P120) → no data from other patients appears.

Guardrails: the patient id is injected by the API (never chosen by the LLM); cited ids not in the retrieved set are dropped; answers without valid evidence become the insufficient-evidence message.
