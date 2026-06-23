"""Prompt stage: retrieved context -> generation prompt string.

Swap prompt variants by name via the ``PROMPTS`` registry. Iterating on a prompt
is just adding a registry entry.

    from prompts import PROMPTS
    prompt_text = PROMPTS.get("v1")(context)
"""

from prompts.builders import PROMPTS

# Import for side effect: registers the shipped prompt variants.
import prompts.builders  # noqa: F401

__all__ = ["PROMPTS"]
