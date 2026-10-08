from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.agent import tools
from app.agent.graph import ask

app = FastAPI(title="Patient 360 API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://localhost:3000"],
                   allow_methods=["*"], allow_headers=["*"])


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


class Ask(BaseModel):
    question: str


def _require(patient_id: str):
    if not tools.get_patient(patient_id):
        raise HTTPException(404, f"Unknown patient {patient_id}")


@app.get("/patients")
def patients():
    from app.db import query
    return query("SELECT * FROM patient ORDER BY id")


@app.get("/patients/{patient_id}/summary")
def summary(patient_id: str):
    _require(patient_id)
    return tools.summary(patient_id)


@app.get("/patients/{patient_id}/observations")
def observations(patient_id: str, name: str | None = None):
    _require(patient_id)
    return tools.get_observations(patient_id, name=name)


@app.post("/patients/{patient_id}/ask")
def ask_question(patient_id: str, body: Ask):
    _require(patient_id)
    if not body.question.strip():
        raise HTTPException(422, "Question is empty")
    try:
        return ask(patient_id, body.question)
    except Exception as e:  # e.g. missing API key
        raise HTTPException(502, f"Agent error: {e}")
