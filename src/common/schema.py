"""The structured document contract produced by the generation stage.

Ported from ``~/rag-testing/generate_synthetic_intake.py`` and matching
VisionDrafter's ``ClarificationContext`` (src/store/GlobalStates.ts). Hyphenated
aliases are the on-the-wire field names; ``populate_by_name=True`` lets you build
instances with either the python name or the alias.

This module is fully implemented — it defines the target schema the generation
prompt fills in.
"""

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class Adversary(BaseModel):
    name: str
    address: str
    relationship: str


class Witness(BaseModel):
    name: str
    address: str
    testimony: str


class IntakeForm(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    client_name: str = Field(alias="client-name")
    client_address: str = Field(alias="client-address")
    client_role: Literal[
        "I am the person affected",
        "I am responding to a complaint or accusation",
        "I am a witness",
    ] = Field(alias="client-role")

    roleOther: str

    adversaries: List[Adversary]
    witnesses: List[Witness]

    incident_description: str = Field(alias="incident-description")
    incident_when: str = Field(alias="incident-when")
    incident_where: str = Field(alias="incident-where")
    incident_damages: str = Field(alias="incident-damages")
    desired_outcome: str = Field(alias="desired-outcome")
    prior_actions: str = Field(alias="prior-actions")


# Fields used as individual per-field retrieval queries (see retrieval/per_field.py).
# These mirror the query fields in ~/rag-testing/tfidf_rag_test.py.
INTAKE_FIELDS: list[str] = [
    "incident-description",
    "incident-when",
    "incident-where",
    "incident-damages",
    "desired-outcome",
    "prior-actions",
]
