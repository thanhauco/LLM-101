from __future__ import annotations

from pathlib import Path

import fitz


def load_pdf_text(path: str | Path) -> str:
    document = fitz.open(path)
    pages = [page.get_text("text") for page in document]
    return "\n".join(pages)


def load_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")
