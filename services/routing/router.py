from __future__ import annotations

import os
from dataclasses import dataclass

from pydantic import BaseModel


class RoutingRequest(BaseModel):
    task: str
    requested_model: str | None = None
    context_tokens: int = 0
    requires_tools: bool = False


class RoutingDecision(BaseModel):
    model: str
    reason: str
    max_context_tokens: int


@dataclass(frozen=True)
class ModelRouter:
    small_model: str
    general_model: str
    coding_model: str
    long_context_model: str

    @classmethod
    def from_env(cls) -> "ModelRouter":
        return cls(
            small_model=os.getenv("SMALL_MODEL", "qwen-4b"),
            general_model=os.getenv("DEFAULT_CHAT_MODEL", "qwen-local"),
            coding_model=os.getenv("CODING_MODEL", "deepseek-coder-local"),
            long_context_model=os.getenv("LONG_CONTEXT_MODEL", "qwen-long-context"),
        )

    def select(self, request: RoutingRequest) -> RoutingDecision:
        if request.requested_model:
            return RoutingDecision(
                model=request.requested_model,
                reason="explicit user or caller selection",
                max_context_tokens=32768,
            )
        if request.context_tokens > 24000:
            return RoutingDecision(
                model=self.long_context_model,
                reason="large context window required",
                max_context_tokens=131072,
            )
        if request.task in {"coding", "patch", "repo"}:
            return RoutingDecision(
                model=self.coding_model,
                reason="coding task routed to coding-specialized model",
                max_context_tokens=32768,
            )
        if request.task in {"summarize", "classify"} and not request.requires_tools:
            return RoutingDecision(
                model=self.small_model,
                reason="cheap small model is enough for low-risk task",
                max_context_tokens=8192,
            )
        return RoutingDecision(
            model=self.general_model,
            reason="default general assistant route",
            max_context_tokens=32768,
        )
