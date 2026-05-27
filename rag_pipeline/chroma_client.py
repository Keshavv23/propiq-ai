import chromadb
from chromadb.config import Settings
from app.config import settings as app_settings

_client = None

def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=app_settings.chroma_persist_path
        )
    return _client

def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="propiq_listings",
        metadata={"hnsw:space": "cosine"}
    )