from datetime import date

from sqlalchemy import create_engine, text

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, future=True)


def query(sql: str, **params) -> list[dict]:
    """Run a SELECT and return rows as plain dicts (dates as ISO strings)."""
    with engine.connect() as conn:
        rows = conn.execute(text(sql), params).mappings().all()
    return [{k: (v.isoformat() if isinstance(v, date) else v) for k, v in r.items()} for r in rows]
