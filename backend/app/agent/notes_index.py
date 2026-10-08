"""ChromaDB collection of clinical notes, embedded with a BGE sentence-transformer."""
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from app.config import CHROMA_PATH, EMBED_MODEL

_client = None
_embed = None
NAME = "clinical_notes"

# two distinct types of data collection systems used to monitor, observe, and evaluate the database

#Connect to ChromaDB
def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH, settings=Settings(anonymized_telemetry=False))
    return _client

# Load the embedding model
def _embedder():
    global _embed
    if _embed is None:
        _embed = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    return _embed

#  Beijing Academy of Artificial Intelligence (BAAI) 
# Connect the above two and get your clinical-notes collection
# get_collection() gives you the configured clinical_notes vector collection that uses BGE embeddings and cosine-based vector similarity.
def get_collection():
    return _get_client().get_or_create_collection(NAME, embedding_function=_embedder(), metadata={"hnsw:space": "cosine"})

# Delete the collection when you need to rebuild it
def reset_collection():
    try:
        _get_client().delete_collection(NAME)
    except Exception:
        pass
