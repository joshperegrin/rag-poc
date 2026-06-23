"""Embedding model for the vector store.

STUB. Implement the body yourself.
"""

from __future__ import annotations

from common.config import settings


def get_embeddings():
    """Return a LangChain ``Embeddings`` backed by the remote Ollama host.

    Plan: ``OllamaEmbeddings(base_url=settings.ollama_base_url,
    model=settings.ollama_embed_model)``.
    """
    # TODO: from langchain_ollama import OllamaEmbeddings; construct and return it.
    raise NotImplementedError("TODO: return OllamaEmbeddings for the remote host")
