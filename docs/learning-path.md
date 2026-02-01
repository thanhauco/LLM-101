# Learning Path

## Phase 1: Model Internals

- Tokenization and token IDs
- Chat templates and role formatting
- Prefill versus decode
- KV cache intuition
- Quantization tradeoffs

## Phase 2: Local Serving

- Run llama.cpp for GGUF models
- Run vLLM as an OpenAI-compatible server
- Stream responses through FastAPI
- Compare latency across model sizes

## Phase 3: RAG

- Parse and chunk documents
- Generate BGE or Qwen embeddings
- Store vectors in Qdrant
- Retrieve, rerank, and generate grounded answers

## Phase 4: Agents and Tools

- Build LangGraph state machines
- Add retrieval, tool calling, and memory
- Create a coding assistant and document assistant
- Add model routing for task-specific behavior

## Phase 5: Production Quality

- Run Ragas and DeepEval checks
- Benchmark coding, JSON, RAG, reasoning, and tool-use tasks
- Add Prometheus metrics and Grafana dashboards
- Explore speculative decoding, batching, TensorRT, and distributed serving
