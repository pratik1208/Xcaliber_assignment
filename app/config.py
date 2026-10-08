import os

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2:///patient360")
CHROMA_PATH = os.getenv("CHROMA_PATH", str(ROOT / "chroma_data"))
SEED_DIR = Path(os.getenv("SEED_DIR", ROOT / "data" / "seed"))
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")
