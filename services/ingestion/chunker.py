from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_document(document: str, chunk_size: int = 800, chunk_overlap: int = 150) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(document)


if __name__ == "__main__":
    sample = "RAG combines retrieval with generation. " * 80
    for chunk in chunk_document(sample):
        print(len(chunk), chunk[:72])
