from app.agent import tools


def test_hba1c_trend_p001():
    vals = [o["value"] for o in tools.get_observations("P001", name="HbA1c")]
    assert vals[0] == 8.2 and vals[-1] == 7.1


def test_active_meds_exclude_stopped():
    names = {m["display"] for m in tools.get_medications("P001", active_only=True)}
    assert "Metformin" in names and "Ibuprofen" not in names


def test_last_three_encounters_newest_first():
    enc = tools.get_encounters("P001", n=3)
    assert [e["id"] for e in enc] == ["E006", "E005", "E004"]


def test_patient_scoping_no_leakage():
    assert not tools.get_observations("P002", name="HbA1c")
    assert all(n["id"].startswith("N1") for n in tools.search_notes("P002", "diabetes"))


def test_note_search_finds_eye_exam():
    ids = {n["id"] for n in tools.search_notes("P001", "unresolved eye exam referral", k=3)}
    assert ids & {"N003", "N005", "N006"}


def test_get_record_roundtrip_and_scope():
    assert tools.get_record("obs:O010", "P001")["value"] == 7.1
    assert tools.get_record("obs:O010", "P002") is None


def test_summary_shape():
    s = tools.summary("P001")
    assert s["patient"]["name"] and len(s["encounters"]) == 3 and s["conditions"]
