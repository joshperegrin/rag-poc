"""Shared contracts used across every stage.

These are the only fully-implemented pieces of the template: the plug-in
mechanism (`Registry`), the document contract (`IntakeForm`), the uniform
retrieval result types, and env-driven settings. Everything in the stage
packages (ingestion/chunking/vectorstore/retrieval/prompts/generation) is a
stub that builds on these.
"""

from common.config import Settings, settings
from common.registry import Registry
from common.schema import Adversary, Witness, IntakeForm, INTAKE_FIELDS
from common.types import ScoredChunk, RetrievalResult

__all__ = [
    "Settings",
    "settings",
    "Registry",
    "Adversary",
    "Witness",
    "IntakeForm",
    "INTAKE_FIELDS",
    "ScoredChunk",
    "RetrievalResult",
]
