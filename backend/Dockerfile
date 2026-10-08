FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Pre-download the BGE embedding model so first start is fast
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"
COPY . .
CMD ["sh", "-c", "python scripts/generate_data.py && python scripts/ingest.py && uvicorn app.api.main:app --host 0.0.0.0 --port 8000"]
