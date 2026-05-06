from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter

from prometheus_client import Counter, Gauge, Histogram

TOKENS = Counter("llm_tokens_total", "Generated and prompt tokens", ["model", "type"])
LATENCY = Histogram("llm_latency_seconds", "Inference latency", ["model", "route"])
TOKENS_PER_SECOND = Gauge("llm_tokens_per_second", "Model throughput", ["model"])
VRAM_USED = Gauge("llm_vram_used_bytes", "Approximate VRAM used by the model", ["model"])
KV_CACHE_TOKENS = Gauge("llm_kv_cache_tokens", "Tokens currently represented in KV cache", ["model"])


@contextmanager
def track_latency(model: str, route: str):
    start = perf_counter()
    try:
        yield
    finally:
        LATENCY.labels(model, route).observe(perf_counter() - start)
