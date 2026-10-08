"""Write the synthetic demo dataset (simplified FHIR-style) to data/seed/.

Deterministic and hand-authored: P001 is the hero patient (diabetes, HbA1c 8.2 -> 7.1),
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


def write(name, rows):
    (SEED / f"{name}.json").write_text(json.dumps(rows, indent=2))


def main():
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
