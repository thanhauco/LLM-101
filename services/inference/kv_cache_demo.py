from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecodeStep:
    token_index: int
    new_attention_work: int
    cached_attention_work: int


def estimate_decode_work(prompt_tokens: int, generated_tokens: int) -> list[DecodeStep]:
    steps: list[DecodeStep] = []
    for index in range(generated_tokens):
        full_context = prompt_tokens + index
        steps.append(
            DecodeStep(
                token_index=index + 1,
                new_attention_work=full_context,
                cached_attention_work=1,
            )
        )
    return steps


def main() -> None:
    steps = estimate_decode_work(prompt_tokens=128, generated_tokens=8)
    print("token,new_attention_work,cached_attention_work")
    for step in steps:
        print(f"{step.token_index},{step.new_attention_work},{step.cached_attention_work}")


if __name__ == "__main__":
    main()
