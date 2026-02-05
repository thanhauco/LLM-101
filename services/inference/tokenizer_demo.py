from __future__ import annotations

import os

from transformers import AutoTokenizer


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(
        os.getenv("TOKENIZER_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    )
    text = "KV cache is working memory"
    tokens = tokenizer.tokenize(text)
    token_ids = tokenizer.encode(text)

    print("Text:", text)
    print("Tokens:", tokens)
    print("Token IDs:", token_ids)
    print("Approx context usage:", len(token_ids), "tokens")


if __name__ == "__main__":
    main()
