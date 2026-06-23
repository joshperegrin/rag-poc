"""Vector store stage: embed chunks and persist/search them in LanceDB."""

from vectorstore.embeddings import get_embeddings
from vectorstore.lancedb_store import connect, create_table, upsert, search

__all__ = ["get_embeddings", "connect", "create_table", "upsert", "search"]
