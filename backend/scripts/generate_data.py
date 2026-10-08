"""Write the synthetic demo dataset (simplified FHIR-style) to data/seed/.

P001/P002 are hand-authored; P003+ are generated (seeded). P001 is the hero patient (diabetes, HbA1c 8.2 -> 7.1),
P002 is a contrasting patient (CKD, no diabetes) used to show patient switching and
questions the record cannot answer.
"""
import json
from pathlib import Path

SEED = Path(__file__).resolve().parent.parent / "data" / "seed"

patients = [
    {"id": "P001", "name": "Maria Alvarez", "birth_date": "1968-03-14", "sex": "female"},
    {"id": "P002", "name": "James Whitfield", "birth_date": "1955-11-02", "sex": "male"},
]

# id, patient, date, type, reason, provider
encounters = [
    ("E001", "P001", "2025-10-14", "outpatient", "Type 2 diabetes follow-up", "Dr. Chen"),
    ("E002", "P001", "2025-12-02", "emergency", "Hyperglycemia, polyuria and fatigue", "Dr. Okafor"),
    ("E003", "P001", "2026-01-20", "outpatient", "Post-ER diabetes follow-up", "Dr. Chen"),
    ("E004", "P001", "2026-04-15", "outpatient", "Diabetes and hypertension review", "Dr. Chen"),
    ("E005", "P001", "2026-07-22", "outpatient", "Diabetes quarterly review", "Dr. Chen"),
    ("E006", "P001", "2026-09-18", "outpatient", "Hypertension check", "Dr. Chen"),
    ("E101", "P002", "2025-11-05", "outpatient", "CKD stage 3 monitoring", "Dr. Patel"),
    ("E102", "P002", "2026-03-10", "outpatient", "CKD follow-up, anemia work-up", "Dr. Patel"),
    ("E103", "P002", "2026-08-25", "outpatient", "CKD follow-up", "Dr. Patel"),
]

# id, patient, code(ICD-10), display, status, onset, encounter
conditions = [
    ("C001", "P001", "E11.9", "Type 2 diabetes mellitus", "active", "2023-02-10", "E001"),
    ("C002", "P001", "I10", "Essential hypertension", "active", "2021-06-01", "E004"),
    ("C003", "P001", "E78.5", "Hyperlipidemia", "active", "2022-09-15", "E004"),
    ("C004", "P001", "J20.9", "Acute bronchitis", "resolved", "2024-01-08", None),
    ("C101", "P002", "N18.3", "Chronic kidney disease, stage 3", "active", "2022-04-20", "E101"),
    ("C102", "P002", "D63.1", "Anemia in chronic kidney disease", "active", "2026-03-10", "E102"),
    ("C103", "P002", "I10", "Essential hypertension", "active", "2018-05-12", "E101"),
]

# id, patient, display, dose, status, start, end, encounter
medications = [
    ("M001", "P001", "Metformin", "1000 mg twice daily", "active", "2023-02-10", None, "E001"),
    ("M002", "P001", "Lisinopril", "10 mg daily", "active", "2021-06-01", None, "E004"),
    ("M003", "P001", "Atorvastatin", "20 mg daily", "active", "2022-09-15", None, "E004"),
    ("M004", "P001", "Ibuprofen", "400 mg as needed", "stopped", "2025-06-01", "2026-01-20", "E003"),
    ("M101", "P002", "Amlodipine", "5 mg daily", "active", "2018-05-12", None, "E101"),
    ("M102", "P002", "Ferrous sulfate", "325 mg daily", "active", "2026-03-10", None, "E102"),
    ("M103", "P002", "Naproxen", "500 mg twice daily", "stopped", "2024-02-01", "2025-11-05", "E101"),
]

# id, patient, encounter, date, name, value, unit
observations = [
    ("O001", "P001", "E001", "2025-10-14", "HbA1c", 8.2, "%"),
    ("O002", "P001", "E001", "2025-10-14", "Fasting glucose", 168, "mg/dL"),
    ("O003", "P001", "E002", "2025-12-02", "Glucose", 412, "mg/dL"),
    ("O004", "P001", "E002", "2025-12-02", "HbA1c", 8.6, "%"),
    ("O005", "P001", "E003", "2026-01-20", "HbA1c", 7.8, "%"),
    ("O006", "P001", "E003", "2026-01-20", "Fasting glucose", 141, "mg/dL"),
    ("O007", "P001", "E004", "2026-04-15", "HbA1c", 7.4, "%"),
    ("O008", "P001", "E004", "2026-04-15", "LDL cholesterol", 96, "mg/dL"),
    ("O009", "P001", "E004", "2026-04-15", "Systolic blood pressure", 138, "mmHg"),
    ("O010", "P001", "E005", "2026-07-22", "HbA1c", 7.1, "%"),
    ("O011", "P001", "E005", "2026-07-22", "Fasting glucose", 124, "mg/dL"),
    ("O012", "P001", "E005", "2026-07-22", "Creatinine", 0.9, "mg/dL"),
    ("O013", "P001", "E006", "2026-09-18", "Systolic blood pressure", 128, "mmHg"),
    ("O101", "P002", "E101", "2025-11-05", "eGFR", 46, "mL/min/1.73m2"),
    ("O102", "P002", "E101", "2025-11-05", "Creatinine", 1.7, "mg/dL"),
    ("O103", "P002", "E102", "2026-03-10", "eGFR", 43, "mL/min/1.73m2"),
    ("O104", "P002", "E102", "2026-03-10", "Hemoglobin", 10.2, "g/dL"),
    ("O105", "P002", "E103", "2026-08-25", "eGFR", 44, "mL/min/1.73m2"),
    ("O106", "P002", "E103", "2026-08-25", "Hemoglobin", 11.0, "g/dL"),
]

# id, patient, encounter, date, display
procedures = [
    ("PR001", "P001", "E002", "2025-12-02", "Intravenous fluid resuscitation"),
    ("PR002", "P001", "E003", "2026-01-20", "Comprehensive diabetic foot exam"),
    ("PR003", "P001", "E004", "2026-04-15", "12-lead electrocardiogram"),
    ("PR101", "P002", "E102", "2026-03-10", "Renal ultrasound"),
]

# id, patient, encounter, date, text
notes = [
    ("N001", "P001", "E001", "2025-10-14",
     "Diabetes follow-up. Patient reports increased thirst and occasional missed evening metformin doses. "
     "HbA1c 8.2%, fasting glucose 168. Reviewed diet and adherence. Continue metformin 1000 mg twice daily. "
     "Recheck HbA1c in 3 months."),
    ("N002", "P001", "E002", "2025-12-02",
     "Emergency visit for 3 days of polyuria, fatigue and blurred vision. Glucose 412 mg/dL, HbA1c 8.6%. "
     "No ketones. Treated with IV fluids and discharged after glucose improved. Patient admits poor diet "
     "over the holidays. Advised to follow up with primary care within 2 weeks."),
    ("N003", "P001", "E003", "2026-01-20",
     "Post-ER follow-up. Glucose logs improving, patient now taking metformin consistently. HbA1c 7.8%. "
     "Foot exam normal. Ibuprofen discontinued. Patient reports mild numbness in both feet at night; "
     "to be monitored. Referred for annual dilated retinal eye exam."),
    ("N004", "P001", "E004", "2026-04-15",
     "Diabetes and blood pressure review. HbA1c 7.4%, LDL 96, BP 138 systolic. ECG unremarkable. "
     "Patient exercising 3 times a week. Metformin continued. Eye exam referral still outstanding."),
    ("N005", "P001", "E005", "2026-07-22",
     "Quarterly review. HbA1c 7.1%, fasting glucose 124, creatinine 0.9. Patient doing well on metformin. "
     "Reports continued foot numbness, unchanged. Retinal eye exam has not been completed; patient to "
     "schedule. Follow up in 3 months."),
    ("N006", "P001", "E006", "2026-09-18",
     "Blood pressure check, 128 systolic on lisinopril. No complaints. Reminded patient about pending "
     "retinal eye exam."),
    ("N101", "P002", "E101", "2025-11-05",
     "CKD stage 3 monitoring. eGFR 46, creatinine 1.7. Naproxen stopped due to kidney function. "
     "Blood pressure controlled on amlodipine."),
    ("N102", "P002", "E102", "2026-03-10",
     "eGFR 43, hemoglobin 10.2. Renal ultrasound ordered. Iron supplementation started for anemia. "
     "Patient concerned about fatigue."),
    ("N103", "P002", "E103", "2026-08-25",
     "eGFR stable at 44, hemoglobin improved to 11.0 on iron. Fatigue improved. Continue monitoring."),
]


# ---------------------------------------------------------------------------
# Bulk synthetic patients (P003..P120). Deterministic via a fixed seed.
# ---------------------------------------------------------------------------
import random
from datetime import date, timedelta

N_PATIENTS = 120
FIRST = ["Olivia", "Liam", "Emma", "Noah", "Ava", "Elijah", "Sophia", "Lucas", "Isabella", "Mason", "Mia", "Ethan",
         "Amelia", "Logan", "Harper", "Aiden", "Evelyn", "Jackson", "Abigail", "Sebastian", "Priya", "Arjun", "Wei",
         "Mei", "Carlos", "Sofia", "Omar", "Fatima", "Kenji", "Yuki", "Grace", "Henry", "Nora", "Samuel", "Ruth"]
LAST = ["Smith", "Johnson", "Garcia", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas",
        "Jackson", "White", "Harris", "Martin", "Thompson", "Lee", "Walker", "Hall", "Young", "Patel", "Nguyen", "Kim",
        "Singh", "Lopez", "Hernandez", "Clark", "Lewis", "Robinson", "Allen", "Scott", "Green", "Baker", "Adams"]
PROVIDERS = ["Dr. Chen", "Dr. Okafor", "Dr. Patel", "Dr. Rivera", "Dr. Lindqvist", "Dr. Nakamura", "Dr. Abdi"]

# name, unit, value when poorly controlled, value when well controlled, decimals
PROFILES = {
    "diabetes": dict(cond=("E11.9", "Type 2 diabetes mellitus"),
                     meds=[("Metformin", "1000 mg twice daily"), ("Metformin", "500 mg twice daily"),
                           ("Glipizide", "5 mg daily"), ("Insulin glargine", "20 units nightly")],
                     labs=[("HbA1c", "%", 9.4, 6.7, 1), ("Fasting glucose", "mg/dL", 190, 116, 0)],
                     visit="Type 2 diabetes follow-up", er="Hyperglycemia with polyuria and fatigue",
                     procs=["Comprehensive diabetic foot exam", "Dilated retinal eye exam"]),
    "hypertension": dict(cond=("I10", "Essential hypertension"),
                         meds=[("Lisinopril", "10 mg daily"), ("Amlodipine", "5 mg daily"), ("Losartan", "50 mg daily")],
                         labs=[("Systolic blood pressure", "mmHg", 158, 122, 0)],
                         visit="Hypertension check", er="Hypertensive urgency with headache",
                         procs=["12-lead electrocardiogram"]),
    "ckd": dict(cond=("N18.3", "Chronic kidney disease, stage 3"),
                meds=[("Amlodipine", "5 mg daily"), ("Sodium bicarbonate", "650 mg twice daily")],
                labs=[("eGFR", "mL/min/1.73m2", 36, 54, 0), ("Hemoglobin", "g/dL", 9.6, 12.2, 1)],
                visit="CKD monitoring", er=None, procs=["Renal ultrasound"]),
    "hyperlipidemia": dict(cond=("E78.5", "Hyperlipidemia"),
                           meds=[("Atorvastatin", "20 mg daily"), ("Rosuvastatin", "10 mg daily")],
                           labs=[("LDL cholesterol", "mg/dL", 162, 88, 0)],
                           visit="Lipid management visit", er=None, procs=[]),
    "asthma": dict(cond=("J45.909", "Asthma"),
                   meds=[("Albuterol inhaler", "2 puffs as needed"), ("Fluticasone inhaler", "110 mcg twice daily")],
                   labs=[("FEV1 percent predicted", "%", 56, 87, 0)],
                   visit="Asthma follow-up", er="Acute asthma exacerbation with wheezing", procs=["Spirometry"]),
    "heart_failure": dict(cond=("I50.9", "Heart failure"),
                          meds=[("Furosemide", "40 mg daily"), ("Carvedilol", "6.25 mg twice daily")],
                          labs=[("BNP", "pg/mL", 820, 190, 0)],
                          visit="Heart failure follow-up", er="Acute decompensated heart failure with dyspnea",
                          procs=["Transthoracic echocardiogram"]),
}
COMBOS = [["diabetes"], ["diabetes", "hypertension"], ["diabetes", "hypertension", "hyperlipidemia"], ["hypertension"],
          ["hypertension", "hyperlipidemia"], ["ckd", "hypertension"], ["asthma"], ["heart_failure", "hypertension"],
          ["hyperlipidemia"], ["diabetes", "ckd"], ["asthma", "hypertension"]]
CONCERNS = ["Patient reports occasional dizziness on standing.", "Patient reports poor sleep and daytime fatigue.",
            "Patient is worried about the cost of medications.", "Patient reports mild numbness in the feet at night.",
            "Patient reports intermittent chest tightness with exertion; to be monitored.",
            "Patient reports difficulty keeping to the diet plan.", "Patient reports occasional missed doses."]
FOLLOWUPS = ["Pending: retinal eye exam not yet completed.", "Pending: repeat labs in 6 weeks not yet scheduled.",
             "Pending: cardiology referral awaiting appointment.", "Pending: nutrition counselling referral outstanding.",
             "Pending: sleep study referral not yet completed."]
NEUTRAL = ["Reviewed medications and adherence.", "Discussed diet and exercise.", "No new complaints today.",
           "Vitals stable.", "Patient understands the plan."]
STOPPED = [("Ibuprofen", "400 mg as needed"), ("Naproxen", "500 mg twice daily"), ("Hydrochlorothiazide", "25 mg daily"),
           ("Prednisone", "20 mg daily for 5 days")]

TODAY = date(2026, 10, 9)


def fmt_val(v, dec):
    return round(v, dec) if dec else int(round(v))


def bulk(rng):
    n = {"E": 2000, "C": 2000, "M": 2000, "O": 2000, "PR": 2000, "N": 2000}

    def nid(k):
        n[k] += 1
        return f"{k}{n[k]}"

    for i in range(3, N_PATIENTS + 1):
        pid = f"P{i:03d}"
        sex = rng.choice(["female", "male"])
        born = date(rng.randint(1942, 1990), rng.randint(1, 12), rng.randint(1, 28))
        patients.append({"id": pid, "name": f"{rng.choice(FIRST)} {rng.choice(LAST)}", "birth_date": born.isoformat(), "sex": sex})
        profs = rng.choice(COMBOS)
        direction = rng.choice(["improving", "improving", "worsening", "stable"])
        n_enc = rng.randint(3, 6)
        span = rng.randint(180, 400)
        start = TODAY - timedelta(days=span + rng.randint(5, 30))
        dates = sorted({start + timedelta(days=int(span * k / (n_enc - 1)) + rng.randint(-6, 6)) for k in range(n_enc)})
        dates = [d for d in dates if d <= TODAY]
        n_enc = len(dates)
        main = PROFILES[profs[0]]
        enc_ids = [nid("E") for _ in dates]
        er_idx = rng.randint(1, n_enc - 1) if main["er"] and rng.random() < 0.4 else None
        provider = rng.choice(PROVIDERS)
        for k, (eid, d) in enumerate(zip(enc_ids, dates)):
            if k == er_idx:
                encounters.append((eid, pid, d.isoformat(), "emergency", main["er"], rng.choice(PROVIDERS)))
            else:
                reason = " and ".join(PROFILES[x]["visit"] for x in profs[:2]) if k % 2 else main["visit"]
                encounters.append((eid, pid, d.isoformat(), "outpatient", reason, provider))
        # conditions
        for pr in profs:
            code, disp = PROFILES[pr]["cond"]
            onset = (start - timedelta(days=rng.randint(200, 2500))).isoformat()
            conditions.append((nid("C"), pid, code, disp, "active", onset, enc_ids[0]))
        if rng.random() < 0.3:
            conditions.append((nid("C"), pid, "J20.9", "Acute bronchitis", "resolved", (start - timedelta(days=400)).isoformat(), None))
        # medications
        for pr in profs:
            drug, dose = rng.choice(PROFILES[pr]["meds"])
            if not any(m[1] == pid and m[2] == drug for m in medications):
                medications.append((nid("M"), pid, drug, dose, "active", (start - timedelta(days=rng.randint(100, 1500))).isoformat(), None, enc_ids[0]))
        if rng.random() < 0.3:
            drug, dose = rng.choice(STOPPED)
            k = rng.randint(1, n_enc - 1)
            medications.append((nid("M"), pid, drug, dose, "stopped", (start - timedelta(days=200)).isoformat(), dates[k].isoformat(), enc_ids[k]))
        # observations + notes
        pending = rng.choice(FOLLOWUPS) if rng.random() < 0.5 else None
        concern_at = rng.randint(0, n_enc - 1) if rng.random() < 0.6 else None
        for k, (eid, d) in enumerate(zip(enc_ids, dates)):
            t = k / max(n_enc - 1, 1)
            sentences = []
            for pr in profs:
                for (lab, unit, bad, good, dec) in PROFILES[pr]["labs"]:
                    if k == 0 or rng.random() < 0.75:
                        frac = {"improving": 1 - t, "worsening": t, "stable": 0.5}[direction]
                        v = good + (bad - good) * frac + rng.uniform(-0.04, 0.04) * (bad - good)
                        v = fmt_val(v, dec)
                        observations.append((nid("O"), pid, eid, d.isoformat(), lab, v, unit))
                        sentences.append(f"{lab} {v}{'' if unit == '%' else ' '}{unit}.".replace("%.", "%."))
            if k == er_idx:
                sentences.insert(0, f"Seen in the emergency department for {main['er'].lower()}. Treated and discharged.")
            else:
                sentences.insert(0, f"Routine {PROFILES[profs[0]]['visit'].lower()}.")
            sentences.append(rng.choice(NEUTRAL))
            if k == concern_at:
                sentences.append(rng.choice(CONCERNS))
            if pending and k >= n_enc - 2:
                sentences.append(pending)
            notes.append((nid("N"), pid, eid, d.isoformat(), " ".join(sentences)))
        # procedures
        pool = [x for pr in profs for x in PROFILES[pr]["procs"]]
        for x in rng.sample(pool, min(len(pool), rng.randint(0, 2))):
            k = rng.randint(0, n_enc - 1)
            procedures.append((nid("PR"), pid, enc_ids[k], dates[k].isoformat(), x))


def write(name, rows):
    (SEED / f"{name}.json").write_text(json.dumps(rows, indent=2))


def main():
    bulk(random.Random(42))
    SEED.mkdir(parents=True, exist_ok=True)
    (SEED / "notes").mkdir(exist_ok=True)
    write("patients", patients)
    write("encounters", [dict(zip(("id", "patient_id", "date", "type", "reason", "provider"), r)) for r in encounters])
    write("conditions", [dict(zip(("id", "patient_id", "code", "display", "status", "onset_date", "encounter_id"), r)) for r in conditions])
    write("medications", [dict(zip(("id", "patient_id", "display", "dose", "status", "start_date", "end_date", "encounter_id"), r)) for r in medications])
    write("observations", [dict(zip(("id", "patient_id", "encounter_id", "date", "name", "value", "unit"), r)) for r in observations])
    write("procedures", [dict(zip(("id", "patient_id", "encounter_id", "date", "display"), r)) for r in procedures])
    index = []
    for nid, pid, eid, date, text in notes:
        (SEED / "notes" / f"{nid}.txt").write_text(text)
        index.append({"id": nid, "patient_id": pid, "encounter_id": eid, "date": date, "file": f"notes/{nid}.txt"})
    write("notes", index)
    print(f"Wrote seed data to {SEED}")


if __name__ == "__main__":
    main()
