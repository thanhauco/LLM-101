from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from openai import OpenAI
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient

from services.embeddings.embed_qdrant import embed_texts
from services.reranker.rerank import rerank


class RagQuery(BaseModel):
    question: str = Field(..., min_length=1)
    collection: str | None = None
    top_k: int = 8
    rerank_k: int = 4
    model: str | None = None


@dataclass
class RagPipeline:
    qdrant: QdrantClient
    openai_client: OpenAI
    collection: str
    default_model: str

    @classmethod
    def from_env(cls, openai_client: OpenAI) -> "RagPipeline":
        return cls(
            qdrant=QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333")),
            openai_client=openai_client,
            collection=os.getenv("QDRANT_COLLECTION", "llms101_docs"),
            default_model=os.getenv("DEFAULT_CHAT_MODEL", "qwen-local"),
        )

    async def answer(self, query: RagQuery) -> dict[str, Any]:
        query_vector = embed_texts([query.question])[0]
        search = self.qdrant.search(
            collection_name=query.collection or self.collection,
            query_vector=query_vector,
            limit=query.top_k,
            with_payload=True,
        )
        passages = [str(point.payload.get("text", "")) for point in search if point.payload]
        ranked = rerank(query.question, passages, limit=query.rerank_k) if passages else []
        context = "\n\n".join(passage for passage, _score in ranked)

        response = self.openai_client.chat.completions.create(
            model=query.model or self.default_model,
            messages=[
                {"role": "system", "content": "Answer only from the provided context."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query.question}"},
            ],
            temperature=0.1,
            max_tokens=600,
        )
        return {
            "answer": response.choices[0].message.content,
            "contexts": [{"text": passage, "score": score} for passage, score in ranked],
        }
