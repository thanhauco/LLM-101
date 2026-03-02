from __future__ import annotations

import os
from collections.abc import Iterable

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer


def embed_texts(texts: list[str], model_name: str | None = None) -> list[list[float]]:
    model = SentenceTransformer(model_name or os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5"))
    return model.encode(texts, normalize_embeddings=True).tolist()


def upsert_chunks(chunks: Iterable[str], collection_name: str | None = None) -> None:
    collection = collection_name or os.getenv("QDRANT_COLLECTION", "llms101_docs")
    chunk_list = list(chunks)
    vectors = embed_texts(chunk_list)
    client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

    client.recreate_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
    )
    client.upsert(
        collection_name=collection,
        points=[
            PointStruct(id=index, vector=vector, payload={"text": text})
            for index, (vector, text) in enumerate(zip(vectors, chunk_list, strict=True))
        ],
    )
