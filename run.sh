#!/usr/bin/env bash
# One-command local run: backend API on :8000, React frontend on :5173. Ctrl+C stops both.
set -euo pipefail
cd "$(dirname "$0")"

# 1. API key
if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
  echo "Created backend/.env — set OPENAI_API_KEY in it, then re-run ./run.sh"
  exit 1
fi
if grep -q "sk-\.\.\." backend/.env || ! grep -q "^OPENAI_API_KEY=" backend/.env; then
  echo "Set a real OPENAI_API_KEY in backend/.env, then re-run."
  exit 1
fi

# 2. Backend env + data
if [ ! -d backend/.venv ]; then
  (cd backend && uv venv --python 3.12 .venv && uv pip install -r requirements.txt)
fi
pg_isready -q || { echo "PostgreSQL is not running (e.g. 'brew services start postgresql@15')."; exit 1; }
psql -lqt | cut -d'|' -f1 | grep -qw patient360 || createdb patient360
(cd backend && .venv/bin/python scripts/generate_data.py && .venv/bin/python scripts/ingest.py)

# 3. Frontend deps
[ -d frontend/node_modules ] || (cd frontend && npm install)

# 4. Start both
(cd backend && .venv/bin/python -m uvicorn app.api.main:app --port 8000) &
API_PID=$!
trap 'kill $API_PID 2>/dev/null' EXIT
sleep 3
echo "API:       http://localhost:8000/docs"
echo "Frontend:  http://localhost:5173"
cd frontend && npm run dev
