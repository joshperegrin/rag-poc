"""Generation-prompt variants.

STUBS. Each builder turns retrieved context into the prompt fed to the generation
stage. Implement the bodies yourself; add a new registry entry to A/B a variant.

Uniform signature:  prompt(context: str, **kw) -> str
"""

from __future__ import annotations

from common.registry import Registry

PROMPTS: Registry = Registry("prompt")

# System framing adapted from VisionDrafter (document_generation/mod.rs FOLLOWUP_SYSTEM)
# and ~/rag-testing/generate_synthetic_intake.py:60+. Edit freely.
SYSTEM = "You are a legal intake assistant for a Philippine law office."


@PROMPTS.register("v1")
def v1(context: str, **kw) -> str:
    """Baseline prompt: instruct the model to fill the IntakeForm from context."""
    # TODO: assemble SYSTEM + instructions + the retrieved `context` into the
    # prompt that drives generation.run(). Return the full prompt string.
    raise NotImplementedError("TODO: implement v1 prompt builder")


@PROMPTS.register("v2")
def v2(context: str, **kw) -> str:
    """Variant for comparison (e.g. stricter grounding / few-shot)."""
    # TODO: implement an alternate phrasing to compare against v1.
    raise NotImplementedError("TODO: implement v2 prompt builder")
