from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SpeculativePlan:
    draft_model: str
    target_model: str
    draft_tokens: int
    acceptance_rate: float

    @property
    def expected_verified_tokens(self) -> float:
        return self.draft_tokens * self.acceptance_rate


def recommend_plan(task: str) -> SpeculativePlan:
    if task == "coding":
        return SpeculativePlan("qwen-coder-1.5b", "deepseek-coder-16b", 8, 0.55)
    return SpeculativePlan("qwen-1.5b", "qwen-14b", 6, 0.65)


if __name__ == "__main__":
    plan = recommend_plan("chat")
    print(plan)
    print("Expected verified tokens:", plan.expected_verified_tokens)
