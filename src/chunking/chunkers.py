"""Chunking strategies.

STUBS. Each chunker takes raw text and returns LangChain ``Document`` objects
tagged with ``{"source", "chunk_index"}``. Implement the bodies yourself; the
signatures and registration are wired so they plug into experiments immediately.

Uniform signature:
    chunker(text: str, *, source: str, **params) -> list[Document]
"""

from __future__ import annotations

import re

from langchain_core.documents import Document

from common.config import settings
from common.registry import Registry

from typing import Callable, TypeAlias

# Function Structure of Chunker:
# text(string): the whole document text
# source(string): where the document is sourced
# chunk_min(int): desired minimum chunks
# chunk_max(int): desired maximum chunks
ChunkerFunc: TypeAlias = Callable[[str, str, int | None, int | None], list[Document]]

CHUNKERS: Registry[ChunkerFunc] = Registry("chunker")

@CHUNKERS.register("paragraph_merge")
def paragraph_merge(text: str, source: str, chunk_min: int | None, chunk_max: int | None) -> list[Document]:
    """Split into small units (paragraphs/lines/sentences) then greedily merge
    only when the document is too big.

    If the document is small, returns units as-is. If large, merges units
    between min/max chars to reduce chunk count.
    """
    min_chars = chunk_min if chunk_min is not None else settings.chunk_min_chars
    max_chars = chunk_max if chunk_max is not None else settings.chunk_max_chars

    # Clean up carriage return, multi tabs, and multi spaces characters
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Split each paragraph into sentence-level units, hard-splitting any single
    # sentence that exceeds max_chars on the nearest preceding word boundary.
    chunks: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph_units: list[str] = []
        for line in re.split(r"\n+", paragraph):
            for sentence in re.split(r"(?<=[.!?])\s+", line):
                remaining_sentence = sentence.strip()
                while len(remaining_sentence) > max_chars:
                    window = remaining_sentence[:max_chars]
                    m = re.search(r"\s(?=\S*$)", window)
                    cut = m.start() if m else max_chars
                    paragraph_units.append(remaining_sentence[:cut].rstrip())
                    remaining_sentence = remaining_sentence[cut:].lstrip()
                if remaining_sentence:
                    paragraph_units.append(remaining_sentence)

        # Greedily merge this paragraph's units into chunks within the
        # [min_chars, max_chars] window.
        current = ""
        for unit in paragraph_units:
            if not current:
                current = unit
                continue
            candidate = current + " " + unit
            if len(candidate) <= max_chars:
                current = candidate
            elif len(current) >= min_chars:
                # current is big enough to stand on its own
                chunks.append(current)
                current = unit
            else:
                # current is below min; accept the oversized merge to reach min
                chunks.append(candidate)
                current = ""
        if current:
            chunks.append(current)

    return [
        Document(page_content=chunk, metadata={"source": source, "chunk_index": i})
        for i, chunk in enumerate(chunks)
    ]

