"""ChromaDB collection of clinical notes, embedded with a BGE sentence-transformer."""
import chromadb
from chromadb.utils import embedding_functions

from app.config import CHROMA_PATH, EMBED_MODEL

_client = None
_embed = None
NAME = "clinical_notes"


def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
    return _client


def _embedder():
    global _embed
    if _embed is None:
        _embed = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    return _embed


def get_collection():
    return _get_client().get_or_create_collection(NAME, embedding_function=_embedder(), metadata={"hnsw:space": "cosine"})


def reset_collection():
    try:
        _get_client().delete_collection(NAME)
    except Exception:
        pass
