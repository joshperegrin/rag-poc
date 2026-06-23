"""LanceDB persistence + vector search.

STUBS. Thin wrappers over ``langchain_community.vectorstores.LanceDB`` using the
embeddings from ``vectorstore.embeddings.get_embeddings``. Implement the bodies
yourself. The ``retrieval`` stage's ``lancedb`` strategy delegates here.
"""

from __future__ import annotations

from langchain_core.documents import Document

from common.config import settings
from common.types import RetrievalResult


def connect(db_path: str | None = None):
    """Open (or create) a LanceDB connection at ``db_path`` (defaults to
    ``settings.lancedb_path``).
    """
    # TODO: import lancedb; return lancedb.connect(db_path or settings.lancedb_path).
    raise NotImplementedError("TODO: open a LanceDB connection")


def create_table(db, name: str):
    """Create or open a LanceDB-backed langchain vector store table."""
    # TODO: build langchain_community.vectorstores.LanceDB(connection=db,
    # table_name=name, embedding=get_embeddings()).
    raise NotImplementedError("TODO: create/open a LanceDB table")


def upsert(table, chunks: list[Document]) -> None:
    """Embed and add ``chunks`` to the table."""
    # TODO: table.add_documents(chunks)
    raise NotImplementedError("TODO: upsert chunks into LanceDB")


def search(table, query: str, k: int = settings.top_k) -> RetrievalResult:
    """Vector-search the table; return results in the uniform RetrievalResult shape."""
    # TODO: run similarity_search_with_score, map hits -> ScoredChunk -> RetrievalResult.
    raise NotImplementedError("TODO: vector search -> RetrievalResult")
