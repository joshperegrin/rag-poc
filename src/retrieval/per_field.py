"""Per-field retrieval + dedup/merge across fields.

STUBS. This is the "individual user response" retrieval shape: each intake field's
value is used as its own query, then chunks hit by multiple fields are deduped and
their metadata merged. Port from ~/rag-testing/tfidf_rag_test.py:363-403
(``build_deduplicated_rag_context``, ``merge_matched_terms``, ``merge_keywords``).
"""

from __future__ import annotations

from common.schema import INTAKE_FIELDS
from common.types import RetrievalResult


def retrieve_per_field(
    retriever,
    field_responses: dict[str, str],
    k: int | None = None,
) -> dict[str, RetrievalResult]:
    """Run one query per intake field.

    Args:
        retriever: any object satisfying the ``Retriever`` protocol.
        field_responses: maps field name (see INTAKE_FIELDS) -> the user's response
            text used as that field's query.
        k: top-k per field.

    Returns:
        field name -> RetrievalResult.
    """
    # TODO: for each field in field_responses (subset of INTAKE_FIELDS),
    # call retriever.query(response, k) and collect.
    raise NotImplementedError("TODO: implement per-field retrieval")


def dedupe_context(per_field: dict[str, RetrievalResult]) -> list[dict]:
    """Collapse per-field results into a deduplicated context.

    A chunk hit by several fields appears once, recording ``matched_fields`` and
    merged metadata, sorted by best score. Mirrors the ``rag_context`` array in
    ~/rag-testing/tfidf_retrieval_results.json.
    """
    # TODO: port build_deduplicated_rag_context (tfidf_rag_test.py:363-403).
    raise NotImplementedError("TODO: implement dedupe/merge of per-field context")


__all__ = ["retrieve_per_field", "dedupe_context", "INTAKE_FIELDS"]
