from __future__ import annotations

import os

from sentence_transformers import CrossEncoder


def rerank(query: str, passages: list[str], limit: int = 5) -> list[tuple[str, float]]:
    model = CrossEncoder(os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-large"))
    pairs = [(query, passage) for passage in passages]
    scores = model.predict(pairs).tolist()
    ranked = sorted(zip(passages, scores, strict=True), key=lambda item: item[1], reverse=True)
    return ranked[:limit]
