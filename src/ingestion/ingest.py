"""PDF -> text with OCR fallback.

STUB. Implement the body yourself.

Plan:
  1. Primary: read the text layer with ``PyPDFLoader`` (pypdf).
  2. Per page with empty/whitespace text, fall back to OCR:
     ``pdf2image.convert_from_path`` -> ``pytesseract.image_to_string``.
  3. Cache the result to ``data/extracted/<name>.txt`` and short-circuit if cached
     (mirrors ~/rag-testing/extracted_texts/).
"""

from __future__ import annotations

from pathlib import Path


def extract_text(pdf_path: str | Path, *, use_cache: bool = True) -> str:
    """Extract full plain text from a PDF, using OCR for pages without a text layer.

    Args:
        pdf_path: path to the source PDF.
        use_cache: read/write the cached .txt under data/extracted/.

    Returns:
        The document's full text.
    """
    # TODO: implement. Reference: ~/rag-testing has the OCR stack pinned
    # (pypdf, pdf2image, pytesseract). Use langchain_community PyPDFLoader for
    # the text layer, then OCR per empty page.
    raise NotImplementedError("TODO: implement PDF text extraction + OCR fallback")
