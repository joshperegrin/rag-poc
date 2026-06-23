"""Uniform return types shared by every retrieval strategy.

Any retriever (bm25, tfidf, lancedb, or one you add) returns a ``RetrievalResult``
so results are directly comparable and any scoring you write later works against
one shape. Fully implemented.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScoredChunk:
    chunk_index: int
    score: float
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrievalResult:
    query: str
    scored_chunks: list[ScoredChunk] = field(default_factory=list)

    def top(self, k: int) -> list[ScoredChunk]:
        return self.scored_chunks[:k]
