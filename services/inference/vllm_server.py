from __future__ import annotations

import os

from vllm import LLM, SamplingParams


def main() -> None:
    llm = LLM(
        model=os.getenv("VLLM_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        tensor_parallel_size=int(os.getenv("VLLM_TENSOR_PARALLEL_SIZE", "1")),
        gpu_memory_utilization=float(os.getenv("VLLM_GPU_MEMORY_UTILIZATION", "0.9")),
    )
    params = SamplingParams(temperature=0.2, top_p=0.9, max_tokens=512)
    outputs = llm.generate(["Explain KV cache in one practical paragraph."], params)
    print(outputs[0].outputs[0].text)


if __name__ == "__main__":
    main()
