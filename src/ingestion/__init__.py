"""Ingestion stage: PDF -> plain text (with OCR fallback)."""

from ingestion.ingest import extract_text

__all__ = ["extract_text"]
