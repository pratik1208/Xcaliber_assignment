"""Retrieval tools. Every tool takes patient_id from the API (never from the LLM) and
returns records tagged with a record_id like 'obs:O010' so answers can cite evidence."""
from app.db import query
from app.agent.notes_index import get_collection


def _tag(rows, kind, prefix):
    for r in rows:
        r["record_id"] = f"{prefix}:{r['id']}"
        r["type"] = kind
    return rows


def get_patient(patient_id):
    return query("SELECT * FROM patient WHERE id = :p", p=patient_id)


def get_encounters(patient_id, n=None, since=None):
    sql = "SELECT * FROM encounter WHERE patient_id = :p AND (CAST(:s AS date) IS NULL OR date >= CAST(:s AS date)) ORDER BY date DESC"
    rows = query(sql + (" LIMIT :n" if n else ""), p=patient_id, s=since, **({"n": n} if n else {}))
    return _tag(rows, "encounter", "enc")


def get_conditions(patient_id, active_only=False):
    sql = "SELECT * FROM condition WHERE patient_id = :p" + (" AND status = 'active'" if active_only else "") + " ORDER BY onset_date DESC"
    return _tag(query(sql, p=patient_id), "condition", "cond")


def get_medications(patient_id, active_only=False):
    sql = "SELECT * FROM medication_request WHERE patient_id = :p" + (" AND status = 'active'" if active_only else "") + " ORDER BY start_date DESC"
    return _tag(query(sql, p=patient_id), "medication", "med")


def get_observations(patient_id, name=None, since=None):
    sql = (
        "SELECT * FROM observation WHERE patient_id = :p "
        "AND (CAST(:n AS text) IS NULL OR name ILIKE '%' || CAST(:n AS text) || '%') "
        "AND (CAST(:s AS date) IS NULL OR date >= CAST(:s AS date)) ORDER BY date ASC"
    )
    return _tag(query(sql, p=patient_id, n=name, s=since), "observation", "obs")


def get_procedures(patient_id, since=None):
    sql = "SELECT * FROM procedure WHERE patient_id = :p AND (CAST(:s AS date) IS NULL OR date >= CAST(:s AS date)) ORDER BY date DESC"
    return _tag(query(sql, p=patient_id, s=since), "procedure", "proc")


def search_notes(patient_id, text, k=4):
    res = get_collection().query(query_texts=[text], n_results=k, where={"patient_id": patient_id})
    out = []
    for nid, doc, meta in zip(res["ids"][0], res["documents"][0], res["metadatas"][0]):
        out.append({"id": nid, "record_id": f"note:{nid}", "type": "note", "date": meta["date"],
                    "encounter_id": meta["encounter_id"], "text": doc})
    return sorted(out, key=lambda r: r["date"])


def get_all_notes(patient_id):
    res = get_collection().get(where={"patient_id": patient_id})
    out = [{"id": i, "record_id": f"note:{i}", "type": "note", "date": m["date"], "encounter_id": m["encounter_id"], "text": d}
           for i, d, m in zip(res["ids"], res["documents"], res["metadatas"])]
    return sorted(out, key=lambda r: r["date"])


def get_record(record_id, patient_id):
    """Resolve a cited record_id back to the stored record (patient-scoped)."""
    kind, _, rid = record_id.partition(":")
    if kind == "note":
        return next((n for n in get_all_notes(patient_id) if n["id"] == rid), None)
    fetch = {"enc": get_encounters, "cond": get_conditions, "med": get_medications, "obs": get_observations, "proc": get_procedures}.get(kind)
    return next((r for r in (fetch(patient_id) if fetch else []) if r["id"] == rid), None)


def summary(patient_id):
    obs = get_observations(patient_id)
    latest = {}
    for o in obs:  # ascending by date -> last wins
        latest[o["name"]] = o
    return {
        "patient": (get_patient(patient_id) or [None])[0],
        "conditions": get_conditions(patient_id, active_only=True),
        "medications": get_medications(patient_id, active_only=True),
        "encounters": get_encounters(patient_id, n=3),
        "observations": sorted(latest.values(), key=lambda o: o["date"], reverse=True),
        "procedures": get_procedures(patient_id)[:3],
    }
