"""Wiring tests for the scaffold.

These assert the structure is sound — registries populated, schema real, stubs
clearly marked — without depending on the (unimplemented) strategy bodies or the
remote Ollama host. Run with: ``pytest`` (pythonpath=src is set in pyproject.toml).
"""

import pytest

from chunking import CHUNKERS
from retrieval import RETRIEVERS
from prompts import PROMPTS
from common.schema import IntakeForm, INTAKE_FIELDS


def test_registries_list_shipped_strategies():
    assert {"paragraph_merge", "by_paragraph", "recursive", "fixed"} <= set(CHUNKERS.names())
    assert {"bm25", "tfidf", "lancedb"} <= set(RETRIEVERS.names())
    assert {"v1", "v2"} <= set(PROMPTS.names())


def test_schema_is_real():
    schema = IntakeForm.model_json_schema()
    assert schema["title"] == "IntakeForm"
    # hyphenated aliases are the on-the-wire names
    assert "incident-description" in schema["properties"]


def test_intake_fields_subset_of_schema():
    aliases = set(IntakeForm.model_json_schema()["properties"])
    assert set(INTAKE_FIELDS) <= aliases


def test_chunker_stub_raises_with_todo():
    with pytest.raises(NotImplementedError, match="TODO"):
        CHUNKERS.get("paragraph_merge")("x", source="y")


def test_unknown_strategy_errors_helpfully():
    with pytest.raises(KeyError, match="available"):
        CHUNKERS.get("does_not_exist")
