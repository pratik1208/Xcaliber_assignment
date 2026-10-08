"""Load seed data: structured JSON -> PostgreSQL (Pandas), notes -> ChromaDB (BGE embeddings)."""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import SEED_DIR  # noqa: E402
from app.db import engine  # noqa: E402
from app.agent.notes_index import get_collection, reset_collection  # noqa: E402

TABLES = {
    "patients": "patient",
    "encounters": "encounter",
    "conditions": "condition",
    "medications": "medication_request",
    "observations": "observation",
    "procedures": "procedure",
}
DATE_COLS = {"birth_date", "date", "onset_date", "start_date", "end_date"}


def load_structured():
    for fname, table in TABLES.items():
        df = pd.DataFrame(json.loads((SEED_DIR / f"{fname}.json").read_text()))
        for col in DATE_COLS & set(df.columns):
            df[col] = pd.to_datetime(df[col]).dt.date
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"  {table}: {len(df)} rows")


def load_notes():
    reset_collection()
    col = get_collection()
    index = json.loads((SEED_DIR / "notes.json").read_text())
    texts = [(SEED_DIR / n["file"]).read_text() for n in index]
    col.add(
        ids=[n["id"] for n in index],
        documents=texts,
        metadatas=[{"patient_id": n["patient_id"], "encounter_id": n["encounter_id"], "date": n["date"]} for n in index],
    )
    print(f"  notes: {len(index)} embedded")


if __name__ == "__main__":
    print("Loading structured data into PostgreSQL...")
    load_structured()
    print("Embedding notes into ChromaDB...")
    load_notes()
    print("Done.")
