"""Chunking stage: text -> list[Document].

Swap strategies by name via the ``CHUNKERS`` registry. Every chunker shares the
signature ``(text: str, *, source: str, **params) -> list[Document]``.

    from chunking import CHUNKERS
    chunks = CHUNKERS.get("paragraph_merge")(text, source="foo")
"""

from chunking.chunkers import CHUNKERS

# Import for side effect: registers the shipped chunker strategies.
import chunking.chunkers  # noqa: F401

__all__ = ["CHUNKERS"]
