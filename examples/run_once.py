"""Smallest end-to-end example: ingestion -> chunking -> retrieval -> generation.

Every stage body is a stub, so running this raises NotImplementedError until you
implement the strategies. It exists to pin the call order and show how the stages
compose. Run from the repo root: ``python examples/run_once.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the code under src/ importable when run from the repo root without `pip install -e .`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ingestion import extract_text
from chunking import CHUNKERS
from retrieval import RETRIEVERS
from retrieval.per_field import retrieve_per_field, dedupe_context
from prompts import PROMPTS
from generation import run as generate
from common.schema import INTAKE_FIELDS

PDF = Path("data/documents/example.pdf")  # drop a PDF here (see ~/rag-testing/legal_documents)


def main() -> None:
    # 1. Ingest
    text = extract_text(PDF)

    # 2. Chunk
    chunks = CHUNKERS.get("paragraph_merge")(text, source=PDF.stem)

    # 3. Retrieve (per intake field, then dedupe across fields)
    retriever = RETRIEVERS.get("bm25")(chunks)
    field_responses = {f: f"<query for {f}>" for f in INTAKE_FIELDS}  # placeholder queries
    per_field = retrieve_per_field(retriever, field_responses)
    context_chunks = dedupe_context(per_field)
    context = "\n\n".join(c["chunk_text"] for c in context_chunks)

    # 4. Generate structured document
    form = generate(PROMPTS.get("v1"), context)
    print(form.model_dump(by_alias=True))


if __name__ == "__main__":
    main()
