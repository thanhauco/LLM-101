from __future__ import annotations

import os

from llama_cpp import Llama


def main() -> None:
    model_path = os.getenv("GGUF_MODEL_PATH", "models/gguf/model.gguf")
    llm = Llama(model_path=model_path, n_ctx=4096, n_gpu_layers=-1)
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are a local assistant."},
            {"role": "user", "content": "Explain quantization in two sentences."},
        ],
        temperature=0.2,
        max_tokens=256,
    )
    print(output["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()
