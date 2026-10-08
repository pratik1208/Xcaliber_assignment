#!/usr/bin/env bash
# One-command local run: sets up venv, database and data, then starts API (8000) and UI (8501).
# Usage: ./run.sh        (Ctrl+C stops both)
set -euo pipefail
cd "$(dirname "$0")"

# 1. API key
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env — edit it and set OPENAI_API_KEY, then re-run ./run.sh"
  exit 1
fi
if grep -q "sk-\.\.\." .env || ! grep -q "API_KEY=" .env; then
  echo "Set a real OPENAI_API_KEY in .env, then re-run."
  exit 1
fi

# 2. Python env
if [ ! -d .venv ]; then
  uv venv --python 3.12 .venv
  uv pip install -r requirements.txt
fi
PY=.venv/bin/python

# 3. Postgres database (local Postgres must be running; set DATABASE_URL in .env to use another)
pg_isready -q || { echo "PostgreSQL is not running. Start it (e.g. 'brew services start postgresql@15')."; exit 1; }
psql -lqt | cut -d'|' -f1 | grep -qw patient360 || createdb patient360

# 4. Data
$PY scripts/generate_data.py
$PY scripts/ingest.py

# 5. Start services
$PY -m uvicorn app.api.main:app --port 8000 &
API_PID=$!
trap 'kill $API_PID 2>/dev/null' EXIT
sleep 3
echo "API:  http://localhost:8000/docs"
echo "UI:   http://localhost:8501"
$PY -m streamlit run app/ui/streamlit_app.py --server.port 8501
