from __future__ import annotations

import os

from transformers import AutoTokenizer


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(
        os.getenv("TOKENIZER_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    )
    messages = [
        {"role": "system", "content": "You are helpful and concise."},
        {"role": "user", "content": "Explain RAG using a tiny example."},
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    print(prompt)


if __name__ == "__main__":
    main()
