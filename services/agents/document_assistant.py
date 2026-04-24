from __future__ import annotations

from services.ingestion.chunker import chunk_document


def build_document_prompt(question: str, document_text: str) -> str:
    chunks = chunk_document(document_text, chunk_size=1200, chunk_overlap=200)
    context = "\n\n".join(chunks[:6])
    return f"Answer from the document context.\n\nContext:\n{context}\n\nQuestion: {question}"
