from __future__ import annotations

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness


def run_rag_eval(samples: list[dict[str, object]]):
    dataset = Dataset.from_list(samples)
    return evaluate(dataset, metrics=[faithfulness, answer_relevancy])


if __name__ == "__main__":
    result = run_rag_eval(
        [
            {
                "question": "What does KV cache store?",
                "answer": "It stores previous key and value tensors for faster decoding.",
                "contexts": ["KV cache stores key and value tensors from prior tokens."],
                "ground_truth": "KV cache stores key and value tensors.",
            }
        ]
    )
    print(result)
