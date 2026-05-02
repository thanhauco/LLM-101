from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    prompt: str
    expected_traits: tuple[str, ...]


BENCHMARKS = [
    BenchmarkCase("coding", "Write a Python function that chunks text.", ("correct", "minimal")),
    BenchmarkCase("json", "Return a JSON object with model and tokens fields.", ("valid_json",)),
    BenchmarkCase("rag", "Answer using only the supplied context.", ("grounded",)),
    BenchmarkCase("reasoning", "Solve a simple planning problem.", ("stepwise",)),
    BenchmarkCase("tool_use", "Choose the right tool for document OCR.", ("tool_choice",)),
]


def run_benchmark(generate) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case in BENCHMARKS:
        start = perf_counter()
        output = generate(case.prompt)
        rows.append(
            {
                "name": case.name,
                "latency_seconds": round(perf_counter() - start, 4),
                "expected_traits": case.expected_traits,
                "output_preview": output[:240],
            }
        )
    return rows
