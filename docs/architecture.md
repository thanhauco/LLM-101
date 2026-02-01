# Architecture

LLMs 101 is organized as a local AI operating system starter. Each layer can run independently while sharing a common API contract.

## Request Flow

1. The web app sends chat, RAG, eval, and model routing requests to FastAPI.
2. FastAPI selects a model through the router and calls an OpenAI-compatible backend.
3. RAG requests embed the query, search Qdrant, rerank passages, and generate a grounded answer.
4. Agents use LangGraph to orchestrate retrieval, tools, memory, and response generation.
5. Metrics flow to Prometheus and Grafana for latency, tokens/sec, VRAM, and cache health.

## Local Services

| Service | Default port | Responsibility |
| --- | --- | --- |
| FastAPI | 8000 | Application gateway |
| vLLM OpenAI server | 8001 | GPU inference |
| Qdrant | 6333 | Vector search |
| Redis | 6379 | Queue and short-lived state |
| Postgres | 5432 | Durable app data |
| MinIO | 9000 | Object storage |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3001 | Dashboards |

## Production Concerns

- Route by task, context length, latency budget, and tool requirements.
- Treat RAG quality as a search system problem before treating it as a model problem.
- Evaluate every prompt, retriever, reranker, and model routing change.
- Track token latency, error rate, retrieval hit rate, and hallucination regressions.
- Sandbox tools and code execution before exposing agents to real systems.
