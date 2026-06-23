# rag-poc

A LangChain RAG experimentation template for testing and evaluating three swappable axes:

- **chunking strategy** — how documents are split (`chunking/`)
- **retrieval strategy** — how chunks are scored/ranked: BM25, TF-IDF, LanceDB vector (`retrieval/`, `vectorstore/`)
- **generation prompt** — how the structured document is drafted (`prompts/`, `generation/`)

The pipeline: ingest PDFs (text + OCR fallback) → chunk → per-field retrieval → generate a structured `IntakeForm` (JSON) via remote **Ollama**.

> **Status: scaffold.** Cross-cutting contracts (`common/`) are implemented; every stage strategy is a clearly-marked `TODO` stub for you to fill in. Reference implementations to port live in `~/rag-testing` (TF-IDF pipeline) and `~/VisionDrafter` (schema/domain).

## Layout (code · notebooks · data · tests separated)

```
src/                  # all package code, divided by stage
  common/             #   registry, schema (IntakeForm), result types, config  — REAL
  ingestion/          #   PDF -> text (+OCR)                                    — stub
  chunking/           #   CHUNKERS registry: paragraph_merge / recursive / ...  — stubs
  vectorstore/        #   OllamaEmbeddings + LanceDB connect/upsert/search      — stubs
  retrieval/          #   RETRIEVERS registry: bm25 / tfidf / lancedb; per-field — stubs
  prompts/            #   PROMPTS registry: v1 / v2 generation prompts          — stubs
  generation/         #   ChatOllama .with_structured_output(IntakeForm)        — stub
data/                 # inputs + generated artifacts (gitignored contents)
  documents/          #   input PDFs
  extracted/          #   cached extracted text
  lancedb/            #   LanceDB tables
notebooks/            # 01_compare_strategies.ipynb — sweep scaffold
tests/                # test_wiring.py — structure/wiring tests (no Ollama needed)
examples/             # run_once.py — minimal end-to-end call order
```

Each axis is a named registry, so swapping a strategy is a one-liner and you can register your own inline:

```python
from chunking import CHUNKERS
from retrieval import RETRIEVERS
from prompts import PROMPTS

chunks    = CHUNKERS.get("paragraph_merge")(text, source="foo")
retriever = RETRIEVERS.get("bm25")(chunks)
hits      = retriever.query("when did the incident happen?", k=5)  # -> RetrievalResult
```

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate    # fish: source .venv/bin/activate.fish
pip install -r requirements.txt
cp .env.example .env                   # set OLLAMA_MODEL / OLLAMA_EMBED_MODEL
# drop PDFs into data/documents/  (samples in ~/rag-testing/legal_documents)
```

Code lives under `src/` and imports by stage (`from chunking import CHUNKERS`). The project is **not** installed as a package — the notebook and `examples/run_once.py` add `src/` to `sys.path`, and `pytest` puts it on the path via `pyproject.toml`.

Run the wiring tests (no Ollama needed — confirms registries are populated and stubs are marked):

```bash
pytest                                 # pythonpath=src configured in pyproject.toml
```

## Where to start implementing

| Stage | File | Port from |
|-------|------|-----------|
| Ingest | `src/ingestion/ingest.py` | `~/rag-testing` OCR stack |
| Chunk | `src/chunking/chunkers.py` | `tfidf_rag_test.py:42-120` |
| Retrieve | `src/retrieval/retrievers.py`, `src/retrieval/per_field.py` | `tfidf_rag_test.py:220-318, 363-403` |
| Vector | `src/vectorstore/*.py` | LangChain `LanceDB` + `OllamaEmbeddings` |
| Prompt | `src/prompts/builders.py` | `generate_synthetic_intake.py:60+` |
| Generate | `src/generation/generate.py` | `generate_synthetic_intake.py:224-270` |
