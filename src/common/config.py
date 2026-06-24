"""Env-driven settings, loaded from a local .env (see .env.example).

Fully implemented and intentionally tiny. Import the module-level ``settings``
singleton, or build your own ``Settings`` for a one-off experiment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    return int(os.getenv(name, default))


def _float(name: str, default: float) -> float:
    return float(os.getenv(name, default))


@dataclass
class Settings:
    # Remote Ollama
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://192.168.1.74:1143")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "")
    ollama_embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "")

    # Generation
    temperature: float = _float("TEMPERATURE", 0.0)
    num_ctx: int = _int("NUM_CTX", 8192)

    # LanceDB
    lancedb_path: str = os.getenv("LANCEDB_PATH", "data/lancedb")

    # Retrieval / chunking defaults
    top_k: int = _int("TOP_K", 5)
    min_score: float = _float("MIN_SCORE", 0.0)
    chunk_min_chars: int = _int("CHUNK_MIN_CHARS", 1000)
    chunk_max_chars: int = _int("CHUNK_MAX_CHARS", 1500)


settings = Settings()
