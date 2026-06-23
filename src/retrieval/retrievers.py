"""Retrieval strategies.

STUBS. Each builder takes the chunked corpus and returns a ``Retriever`` whose
``.query`` produces a uniform ``RetrievalResult``. Implement the bodies yourself;
the registry wiring and the ``Retriever`` protocol are ready.

Builder signature:  (chunks: list[Document]) -> Retriever
Query signature:    Retriever.query(text: str, k: int) -> RetrievalResult
"""

from __future__ import annotations

from typing import Protocol

from langchain_core.documents import Document

from common.config import settings
from common.registry import Registry
from common.types import RetrievalResult, ScoredChunk

RETRIEVERS: Registry = Registry("retriever")


class Retriever(Protocol):
    def query(self, text: str, k: int = settings.top_k) -> RetrievalResult: ...


@RETRIEVERS.register("bm25")
def bm25(chunks: list[Document]) -> Retriever:
    """Lexical BM25. The default; matches the user's per-field plan.

    Plan: build ``BM25Retriever.from_documents(chunks)``
    (langchain_community.retrievers). LangChain hides scores, so reach into the
    underlying ``BM25Okapi.get_scores`` to populate ``ScoredChunk.score`` and to
    threshold by ``settings.min_score`` — keeping the score/rank shape of
    ~/rag-testing/tfidf_retrieval_results.json.
    """
    raise NotImplementedError("TODO: implement BM25 retriever (rank-bm25 / BM25Retriever)")


@RETRIEVERS.register("tfidf")
def tfidf(chunks: list[Document]) -> Retriever:
    """scikit-learn TF-IDF + cosine similarity baseline (the user's current
    approach in ~/rag-testing/tfidf_rag_test.py:220-318). For apples-to-apples
    comparison with bm25."""
    raise NotImplementedError("TODO: implement TF-IDF baseline retriever")


@RETRIEVERS.register("lancedb")
def lancedb(chunks: list[Document]) -> Retriever:
    """Vector retrieval via LanceDB. Delegates to the vectorstore stage:
    connect -> create_table -> upsert(chunks); ``.query`` calls
    ``vectorstore.search``. Lets you compare lexical vs vector (and build hybrid
    later) without changing any caller."""
    raise NotImplementedError("TODO: implement LanceDB retriever (delegates to vectorstore/)")


# --- Reference: a Retriever returning hardcoded sample data ---------------
# Useful as a placeholder while wiring downstream stages. Not registered.
class _SampleRetriever:
    def __init__(self, chunks: list[Document]) -> None:
        self._chunks = chunks

    def query(self, text: str, k: int = settings.top_k) -> RetrievalResult:
        return RetrievalResult(
            query=text,
            scored_chunks=[
                ScoredChunk(chunk_index=0, score=1.0, text="<placeholder chunk>", metadata={})
            ][:k],
        )
