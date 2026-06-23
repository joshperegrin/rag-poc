"""Structured document generation via remote Ollama.

STUB. Implement the body yourself.

Plan:
  - ``ChatOllama(base_url=settings.ollama_base_url, model=settings.ollama_model,
    temperature=settings.temperature)`` from langchain_ollama.
  - ``llm.with_structured_output(IntakeForm)`` so LangChain passes the schema to
    Ollama's ``format`` (cf. ~/rag-testing/generate_synthetic_intake.py:246) and
    returns a validated IntakeForm.
  - Fallback if a model's structured output is weak: prompt for raw JSON, then
    ``extract_first_json_object`` + ``IntakeForm.model_validate_json``
    (generate_synthetic_intake.py:181-198, 259-261).
"""

from __future__ import annotations

from typing import Callable

from common.config import settings
from common.schema import IntakeForm


def run(
    prompt: Callable[..., str],
    context: str,
    *,
    model: str | None = None,
    **prompt_kwargs,
) -> IntakeForm:
    """Generate a structured IntakeForm from retrieved context.

    Args:
        prompt: a prompt builder from the ``PROMPTS`` registry (or your own).
        context: retrieved context string to fill into the prompt.
        model: override ``settings.ollama_model`` for this call.
        **prompt_kwargs: forwarded to the prompt builder.

    Returns:
        A validated ``IntakeForm`` (call ``.model_dump(by_alias=True)`` for JSON).
    """
    # TODO: build prompt_text = prompt(context, **prompt_kwargs); construct
    # ChatOllama; call .with_structured_output(IntakeForm).invoke(prompt_text).
    raise NotImplementedError("TODO: implement Ollama structured generation -> IntakeForm")
