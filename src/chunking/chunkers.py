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

CHUNKERS: Registry = Registry("chunker")


@CHUNKERS.register("paragraph_merge")
def paragraph_merge(text: str, *, source: str, **params) -> list[Document]:
    """Split into small units (paragraphs/lines/sentences) then greedily merge
    into chunks between min/max chars.

    The default strategy, ported from ~/rag-testing/tfidf_rag_test.py:42-120.
    Honors ``min_chars`` / ``max_chars`` from ``params`` (defaults in
    common.config.Settings).
    """
    min_chars = int(params.get("min_chars", settings.chunk_min_chars))
    max_chars = int(params.get("max_chars", settings.chunk_max_chars))

    # Split text into the smallest sensible units: paragraphs -> lines -> sentences.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    units: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        for line in re.split(r"\n+", paragraph):
            line = line.strip()
            if not line:
                continue
            for sentence in re.split(r"(?<=[.!?])\s+", line):
                sentence = sentence.strip()
                if sentence:
                    units.append(sentence)

    # Greedily merge units into chunks between min/max chars.
    chunks: list[str] = []
    current = ""
    for unit in units:
        if not current:
            current = unit
            continue

        candidate = current + " " + unit
        if len(candidate) <= max_chars:
            current = candidate
        elif len(current) >= min_chars:
            # current is big enough on its own; start a new chunk with this unit
            chunks.append(current.strip())
            current = unit
        else:
            # current is too small to stand alone; keep the oversized merge
            chunks.append(candidate.strip())
            current = ""

    if current.strip():
        chunks.append(current.strip())

    return [
        Document(page_content=chunk, metadata={"source": source, "chunk_index": i})
        for i, chunk in enumerate(chunks)
    ]


@CHUNKERS.register("by_paragraph")
def by_paragraph(text: str, *, source: str, **params) -> list[Document]:
    raise NotImplementedError("TODO: implement by_paragraph")


@CHUNKERS.register("recursive")
def recursive(text: str, *, source: str, **params) -> list[Document]:
    """Wrapper around langchain ``RecursiveCharacterTextSplitter``. Honor
    ``chunk_size`` / ``chunk_overlap`` from ``params``."""
    # TODO: implement using langchain_text_splitters.RecursiveCharacterTextSplitter.
    raise NotImplementedError("TODO: implement recursive splitter wrapper")


@CHUNKERS.register("fixed")
def fixed(text: str, *, source: str, **params) -> list[Document]:
    """Fixed-size character windows with overlap. Baseline."""
    # TODO: implement fixed-size + overlap windows.
    raise NotImplementedError("TODO: implement fixed-size chunker")
