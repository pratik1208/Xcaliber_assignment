

# Patient 360 — Clinical Intelligence Agent

## Problem Statement

Healthcare providers spend significant time reviewing fragmented patient information across **encounters, diagnoses, medications, laboratory results, procedures, and clinical notes** to understand a patient's current condition and medical history.

Important information may be distributed across multiple encounters and documents, making it difficult for a physician to quickly answer questions such as:

- What has happened with this patient recently?
- What are the patient's active conditions and medications?
- How have important lab values changed over time?
- What changed between the patient's recent encounters?
- Are there any unresolved clinical issues or follow-ups?
- What did the physician document about a particular condition or concern?

### Objective

Build a **Patient Clinical Intelligence Agent** that provides healthcare providers with a natural-language interface to a patient's longitudinal medical record.

The prototype should allow a physician to select a patient and ask questions about their medical history. The agent should retrieve the relevant patient information, analyze it across time and across different data types, and provide a concise answer supported by the underlying clinical evidence.

### Core Capabilities

The prototype should support:

**1. Patient 360 Summary**

Provide a concise overview of:

- Active conditions
- Current medications
- Recent encounters
- Important observations/lab results
- Recent procedures

**2. Natural-Language Patient Questions**

Allow providers to ask questions such as:

> "What happened during the patient's last three encounters?"

> "What medications is the patient currently taking?"

> "How has the patient's HbA1c changed over the last year?"

> "What concerns were documented during recent visits?"

**3. Longitudinal Analysis**

Connect information across multiple encounters to identify trends and changes, for example:

> "Has the patient's diabetes been improving?"

The system should analyze relevant observations, medications, encounters, and clinical notes rather than relying on a single record.

**4. Clinical Information Retrieval**

Retrieve relevant information from both:

- Structured data — encounters, diagnoses, medications, observations, procedures
- Unstructured data — clinical notes and documents

**5. Evidence and Provenance**

The agent should show the clinical records supporting its answer, such as:

- Encounter date
- Lab/observation
- Medication
- Clinical note

This allows the provider to verify the answer against the original patient record.

**6. Uncertainty Handling**

If the available patient record does not contain sufficient evidence, the system should explicitly state:

> "Insufficient evidence in the available records."

The agent should not infer or invent clinical information that is not supported by the patient's record.

### Example Use Case

A physician selects **Patient P001** and asks:

> **"How has this patient's diabetes progressed over the last year?"**

The agent retrieves:

- Diabetes-related encounters
- HbA1c results
- Diabetes medications
- Relevant diagnoses
- Relevant clinical notes

It analyzes the patient's timeline and responds:

> **"The patient's glycemic control appears to have improved over the last year. HbA1c decreased from 8.2% to 7.1%. The patient had one emergency encounter related to hyperglycemia, followed by subsequent outpatient visits showing lower HbA1c values. Metformin was continued during this period."**

The system then displays the supporting records used to generate the answer.

### Prototype Scope

This prototype will focus on **information retrieval, summarization, longitudinal analysis, and evidence-grounded question answering**.

It will **not**:

- Make autonomous diagnoses
- Prescribe or recommend medications
- Replace physician judgment
- Make treatment decisions

The purpose is to help physicians **find and understand relevant patient information faster**, while keeping the physician in control of clinical decisions.

## Expected Outcome

The prototype should demonstrate that a healthcare provider can interact with a patient's longitudinal record using natural language instead of manually searching through multiple clinical records.

The core value proposition is:

> **"Ask questions about the patient. Get a concise answer, understand the reasoning, and verify it against the underlying clinical evidence."**

## Technology Stack

- **Frontend:** Streamlit — patient dashboard and natural-language chat interface.
- **Backend:** FastAPI — REST APIs and application logic.
- **Agent Framework:** LangGraph — query routing and agent orchestration.
- **LLM:** OpenAI / Claude — question understanding and response generation.
- **Database:** PostgreSQL — structured patient, encounter, medication, and observation data.
- **Vector Database:** ChromaDB — semantic search over clinical notes and documents.
- **Embeddings:** Sentence Transformers / BGE — clinical document embeddings.
- **Data Processing:** Python + Pandas — data ingestion, transformation, and preprocessing.
- **Healthcare Data Model:** Simplified FHIR — Patient, Encounter, Condition, Observation, Medication, and Procedure resources.
- **Deployment:** Docker — containerization and reproducible deployment.
