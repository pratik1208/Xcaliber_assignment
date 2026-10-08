# Patient 360 — Clinical Intelligence Agent (demo)

Ask natural-language questions about a patient's record; get a concise answer plus the cited records.
Stack: Streamlit · FastAPI · LangGraph · Claude/OpenAI · PostgreSQL · ChromaDB (BGE) · Pandas. Synthetic data only.

## Run with Docker
    cp .env.example .env   # add ANTHROPIC_API_KEY
    docker compose up --build      # UI: http://localhost:8501  API: http://localhost:8000/docs

## Run locally (no Docker)
    uv venv --python 3.12 .venv && uv pip install -r requirements.txt
    createdb patient360                       # local Postgres; override with DATABASE_URL
    .venv/bin/python scripts/generate_data.py && .venv/bin/python scripts/ingest.py
    cp .env.example .env                      # add ANTHROPIC_API_KEY
    .venv/bin/uvicorn app.api.main:app --port 8000 &
    .venv/bin/streamlit run app/ui/streamlit_app.py
    .venv/bin/python -m pytest tests          # offline tests (LLM is faked)

## Demo script
1. Pick **P001** → Patient 360 panel loads from SQL (no LLM).
2. "How has this patient's diabetes progressed over the last year?" → improved, HbA1c 8.2% → 7.1%, with HbA1c chart + evidence.
3. "What concerns were documented during recent visits?" / "Are there any unresolved follow-ups?" → cites notes (foot numbness, pending eye exam).
4. "What is the patient's smoking history?" → *Insufficient evidence in the available records.*
5. "Should we increase the metformin dose?" → declines advice, shows relevant records.
6. Switch to **P002** → no P001 data appears; diabetes questions return insufficient evidence.

Guardrails: the patient id is injected by the API (never chosen by the LLM); cited ids not in the retrieved set are dropped; answers without valid evidence become the insufficient-evidence message.
