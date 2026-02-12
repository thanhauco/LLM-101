from __future__ import annotations

import os
from time import perf_counter
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

from services.rag.pipeline import RagPipeline, RagQuery
from services.routing.router import ModelRouter, RoutingRequest

app = FastAPI(title="LLMs 101 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUESTS = Counter("llms101_api_requests_total", "Total API requests", ["route"])
LATENCY = Histogram("llms101_api_latency_seconds", "API route latency", ["route"])

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:8001/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "local-dev-key"),
)
router = ModelRouter.from_env()
rag_pipeline = RagPipeline.from_env(openai_client=client)


class ChatRequest(BaseModel):
    messages: list[dict[str, str]] = Field(..., min_length=1)
    model: str | None = None
    temperature: float = 0.2
    max_tokens: int = 512


class ChatResponse(BaseModel):
    model: str
    content: str
    usage: dict[str, Any] | None = None


class OpenAIChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    model: str
    choices: list[dict[str, Any]]
    usage: dict[str, Any] | None = None


@app.get("/health")
def health() -> dict[str, str]:
    REQUESTS.labels("health").inc()
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest) -> ChatResponse:
    route = "chat"
    REQUESTS.labels(route).inc()
    start = perf_counter()
    selected = router.select(
        RoutingRequest(
            task="chat",
            requested_model=req.model,
            context_tokens=sum(len(message.get("content", "")) for message in req.messages) // 4,
        )
    )

    try:
        response = client.chat.completions.create(
            model=selected.model,
            messages=req.messages,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
    except Exception as exc:  # pragma: no cover - depends on local model server availability
        raise HTTPException(status_code=502, detail=f"Model backend failed: {exc}") from exc
    finally:
        LATENCY.labels(route).observe(perf_counter() - start)

    choice = response.choices[0]
    return ChatResponse(
        model=selected.model,
        content=choice.message.content or "",
        usage=response.usage.model_dump() if response.usage else None,
    )


@app.post("/v1/chat/completions")
async def openai_chat_completions(req: ChatRequest) -> OpenAIChatCompletionResponse:
    response = await chat(req)
    return OpenAIChatCompletionResponse(
        id="chatcmpl-local",
        model=response.model,
        choices=[
            {
                "index": 0,
                "message": {"role": "assistant", "content": response.content},
                "finish_reason": "stop",
            }
        ],
        usage=response.usage,
    )


@app.post("/rag/query")
async def rag_query(req: RagQuery) -> dict[str, Any]:
    REQUESTS.labels("rag_query").inc()
    start = perf_counter()
    try:
        return await rag_pipeline.answer(req)
    finally:
        LATENCY.labels("rag_query").observe(perf_counter() - start)


@app.get("/models/route")
def route_model(task: str = "chat", context_tokens: int = 0) -> dict[str, Any]:
    REQUESTS.labels("model_route").inc()
    selected = router.select(RoutingRequest(task=task, context_tokens=context_tokens))
    return selected.model_dump()


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
