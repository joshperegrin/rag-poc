"""Retrieval stage: documents -> ranked chunks.

Swap strategies by name via the ``RETRIEVERS`` registry. A strategy is a builder
``(chunks: list[Document]) -> Retriever`` whose ``.query(text, k)`` returns a
uniform ``RetrievalResult``.

    from retrieval import RETRIEVERS
    retriever = RETRIEVERS.get("bm25")(chunks)
    result = retriever.query("when did it happen?", k=5)

Per-field helpers (mirroring ~/rag-testing) live in retrieval.per_field.
"""

from retrieval.retrievers import RETRIEVERS, Retriever

# Import for side effect: registers the shipped retriever strategies.
import retrieval.retrievers  # noqa: F401

__all__ = ["RETRIEVERS", "Retriever"]
