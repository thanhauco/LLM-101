# LLMs 101 Reference Repo

LLMs 101 is a local-first reference monorepo for learning how modern LLM systems are put together. It is intentionally shaped like a small local AI operating system: a UI, API gateway, inference adapters, RAG pipeline, agents, evaluation, fine-tuning configs, observability, and local infrastructure.

The core lesson this repo reinforces is that production AI systems usually fail around memory, retrieval, orchestration, and evaluation before they fail because the base model is weak.

## Feature Coverage

| Original idea | Status | Implementation |
| --- | --- | --- |
| Local inference | Implemented starter | `services/inference/vllm_server.py`, `services/inference/llama_cpp_server.py` |
| Tokenizer inspection | Implemented starter | `services/inference/tokenizer_demo.py`, `notebooks/llm101_tokenizer.ipynb` |
| KV cache understanding | Implemented starter | `services/inference/kv_cache_demo.py` |
| Quantization | Implemented starter | `services/inference/quantization_demo.py`, `services/finetune/axolotl_qlora.yml` |
| Chat templates | Implemented starter | `services/inference/chat_template_demo.py` |
| RAG | Implemented starter | `services/rag/pipeline.py` |
| Embeddings | Implemented starter | `services/embeddings/embed_qdrant.py` |
| Reranking | Implemented starter | `services/reranker/rerank.py` |
| Agents and tools | Implemented starter | `services/agents/langgraph_agent.py` |
| Multimodal | Implemented starter | `services/multimodal/vision_ocr.py` |
| OpenAI-compatible serving | Implemented starter | `apps/api/main.py` exposes `/chat` and `/v1/chat/completions`; Compose includes vLLM |
| Evaluation | Implemented starter | `services/evals/run_eval.py` |
| LoRA fine-tuning | Implemented starter | `services/finetune/lora_config.py`, `services/finetune/axolotl_qlora.yml` |
| Observability | Implemented starter | `services/observability/metrics.py`, `infra/monitoring` |
| Benchmark suite | Implemented starter | `services/evals/benchmark_runner.py` |
| vLLM support | Implemented starter | `services/inference/vllm_server.py`, `infra/docker/docker-compose.yml` |
| SGLang support | Implemented starter | `services/inference/sglang_server.py`, `infra/docker/docker-compose.yml` |
| Local coding assistant | Implemented starter | `services/agents/coding_assistant.py` |
| Document assistant | Implemented starter | `services/agents/document_assistant.py` |
| Speculative decoding | Implemented starter | `services/inference/speculative_decoding.py` |
| Model routing | Implemented starter | `services/routing/router.py`, `apps/api/main.py`, web route panel |
| Structured Outputs | Implemented | `services/inference/structured_output_demo.py` |
| Prompt Caching | Implemented | `services/inference/prompt_caching_demo.py` |
| Multi-LoRA Serving | Implemented | `services/inference/multi_lora_demo.py` |
| Corrective RAG (CRAG) | Implemented | `services/rag/corrective_rag.py` |
| GraphRAG | Implemented | `services/rag/graph_rag.py` |
| Sandboxed Code Tool | Implemented | `services/agents/code_sandbox.py` |
| Input/Output Safety | Implemented | `services/guardrails/safety_gate.py` |
| Browser Edge WebGPU | Implemented | `apps/web/app/edge/page.tsx` |

The heavyweight ML examples are intentionally starter implementations. They are ready for local experimentation, but real inference, OCR, fine-tuning, and eval runs require model downloads, hardware-specific setup, and optional dependencies.

## Recommended Stack

| Layer | Tech |
| --- | --- |
| Frontend | Next.js, D3, lucide-react |
| API | FastAPI |
| Inference | vLLM, SGLang, llama.cpp |
| GPU Runtime | CUDA |
| Embeddings | BGE or Qwen Embedding |
| Vector DB | Qdrant |
| Reranker | BGE Reranker |
| Agent Framework | LangGraph |
| OCR | PaddleOCR |
| Parsing | Docling, PyMuPDF |
| Evaluation | Ragas, DeepEval |
| Fine-tuning | Axolotl, Unsloth, PEFT |
| Monitoring | OpenTelemetry, Prometheus, Grafana |
| Auth | Keycloak |
| Queue | Redis |
| Storage | Postgres |
| Object Store | MinIO |

## Monorepo Layout

```text
apps/
  web/           Next.js workbench with D3 diagrams, live feed, chat console, model routing panel
  api/           FastAPI gateway and OpenAI-compatible proxy endpoint
  admin/         Placeholder for model registry, auth, dataset governance, and operations
  playground/    Placeholder for prompt, routing, retrieval, and eval experiments

services/
  inference/     vLLM, SGLang, llama.cpp, tokenizer, chat template, KV cache, quantization, speculative decoding
  embeddings/    BGE/Qwen embedding helpers and Qdrant upsert flow
  reranker/      Cross-encoder reranking example
  rag/           Retrieval, reranking, and grounded answer pipeline
  agents/        LangGraph agent, coding assistant, document assistant
  evals/         Ragas eval runner and benchmark suite
  ingestion/     Document loading and chunking
  multimodal/    Vision processor and PaddleOCR starter
  finetune/      LoRA and QLoRA/Axolotl configs
  observability/ Prometheus metric helpers
  routing/       Model routing policy

models/          GGUF, safetensors, LoRA, and catalog configs
infra/           Docker Compose, Kubernetes notes, Terraform notes, monitoring
datasets/        Eval and instruction-tuning sample data
notebooks/       Concept walkthrough notebooks
scripts/         Bootstrap and model download helpers
docs/            Architecture, learning path, and security notes
```

## Quick Start

1. Copy the environment template:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Install web dependencies:

   ```powershell
   npm install
   ```

3. Start the animated web workbench:

   ```powershell
   npm run dev:web
   ```

   Open `http://localhost:3000`.

4. Create a Python environment and install API dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r apps/api/requirements.txt
   ```

5. Start the local data plane:

   ```powershell
   docker compose --env-file .env -f infra/docker/docker-compose.yml up -d qdrant redis postgres minio prometheus grafana
   ```

6. Start the API:

   ```powershell
   python -m uvicorn main:app --app-dir apps/api --reload --port 8000
   ```

7. Optional GPU serving with vLLM or SGLang:

   ```powershell
   docker compose --env-file .env -f infra/docker/docker-compose.yml --profile gpu up -d vllm
   docker compose --env-file .env -f infra/docker/docker-compose.yml --profile gpu up -d sglang
   ```

## Web Workbench

The Next.js app is the first screen of the project. It includes:

- Chat console wired to the FastAPI `/chat` endpoint.
- Model picker and live model routing panel.
- Animated live feed for retrieval, routing, evaluation, and telemetry events.
- D3 system map showing Prompt, Router, Retrieve, Rerank, Generate, and Evaluate flow.
- D3 telemetry chart showing token throughput and quality gates.
- Responsive layout with reduced-motion support.

## API Endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Basic API health check |
| `POST /chat` | Local chat endpoint that routes to an OpenAI-compatible backend |
| `POST /v1/chat/completions` | Minimal OpenAI-compatible chat response shape |
| `POST /rag/query` | RAG query flow: embed, retrieve, rerank, generate |
| `GET /models/route` | Inspect model routing decisions |
| `GET /metrics` | Prometheus metrics |

## Concept Demos

Run these from the repository root after installing Python dependencies.

```powershell
python services/inference/tokenizer_demo.py
python services/inference/chat_template_demo.py
python services/inference/kv_cache_demo.py
python services/inference/quantization_demo.py
python services/inference/speculative_decoding.py
python services/agents/langgraph_agent.py
```

GPU or model-server examples:

```powershell
python services/inference/vllm_server.py
python services/inference/llama_cpp_server.py
python services/inference/sglang_server.py
```

## Learning Order

1. **Tokens and prompts:** tokenizer IDs, context usage, and chat templates.
2. **Inference internals:** prefill, decode, KV cache, quantization, streaming, vLLM, SGLang, and llama.cpp.
3. **RAG:** ingestion, chunking, embeddings, Qdrant retrieval, reranking, and answer generation.
4. **Agents:** LangGraph orchestration, tool calls, coding assistant, document assistant, and memory shape.
5. **Production quality:** Ragas, DeepEval, benchmark runner, Prometheus, Grafana, and regression tracking.
6. **Optimization:** speculative decoding, batching, TensorRT-style serving ideas, distributed serving, and model routing.

## Recommended Models

| Size | Models | Use |
| --- | --- | --- |
| Small | Qwen 4B, Gemma 4B, Phi | Edge, quick summaries, tiny assistant tasks |
| Medium | Qwen 14B, DeepSeek 16B, Mistral Medium | General chat, coding, RAG, reasoning |
| Large | Qwen 27B, DeepSeek MoE, Nemotron | Agents, coding, enterprise reasoning |

Model binaries are ignored under `models/gguf`, `models/safetensors`, and `models/loras` so the repo stays lightweight.

## Advanced Features (2026 Update)

We have added a suite of production-grade advanced features showcasing modern LLM application patterns:

1. **Structured Outputs & Guided Decoding** ([structured_output_demo.py](file:///c:/Code/LLM-101/services/inference/structured_output_demo.py)): Demonstrates logit-level schema constraints using Pydantic templates, ensuring that the model output conforms to structural formats like SQL queries or JSON parameters.
2. **Context / Prompt Caching** ([prompt_caching_demo.py](file:///c:/Code/LLM-101/services/inference/prompt_caching_demo.py)): Measures Time-to-First-Token (TTFT) acceleration when reusing the prefix KV cache of large documents or system instructions (showing up to 30x latency reduction).
3. **Multi-LoRA Serving** ([multi_lora_demo.py](file:///c:/Code/LLM-101/services/inference/multi_lora_demo.py)): Documents the API payloads and command setup for dynamic hot-swapping of specialized task adapters (like code or math models) on a single shared base model.
4. **Corrective RAG (CRAG)** ([corrective_rag.py](file:///c:/Code/LLM-101/services/rag/corrective_rag.py)): Orchestrates an agentic self-corrective retrieval pipeline via LangGraph, checking context relevance and falling back to a query reformer / web search when local documents are missing.
5. **GraphRAG** ([graph_rag.py](file:///c:/Code/LLM-101/services/rag/graph_rag.py)): Pure-Python entity-relationship mapping and traversal, showing how subgraph retrieval resolves global query questions.
6. **Sandboxed Code Interpreter** ([code_sandbox.py](file:///c:/Code/LLM-101/services/agents/code_sandbox.py)): Restricts agent code execution using isolated subprocesses, timeouts, and error catching for local code assistant tasks.
7. **Input/Output Safety Gate** ([safety_gate.py](file:///c:/Code/LLM-101/services/guardrails/safety_gate.py)): Scans input queries for prompt injection/system overrides and filters outputs for toxic or banned content.
8. **Browser Edge WebGPU** ([page.tsx](file:///c:/Code/LLM-101/apps/web/app/edge/page.tsx)): A Next.js interface implementing offline browser-level inference with Transformers.js and WebGPU support.

## Validation

Current scaffold checks:

```powershell
npm run build:web
python -m compileall apps services scripts
```

The web build validates the D3 dashboard and Next.js app. The Python compile step checks syntax without importing every heavyweight ML dependency.

## Review Result

The original plan has been reviewed against the repository. Every named feature is represented by a file, service, route, config, notebook, or Compose entry. Some components are intentionally starter-level because they depend on local hardware, model downloads, credentials, or large optional packages:

- Real model serving requires vLLM, SGLang, or llama.cpp plus local model files.
- OCR and multimodal examples require PaddleOCR and vision model dependencies.
- Fine-tuning requires Axolotl or Unsloth setup and training data.
- RAG quality depends on loading real documents into Qdrant.
- Keycloak, Redis, Postgres, MinIO, Prometheus, and Grafana are available through Compose but not deeply integrated into every application path yet.

That is the intended boundary for this starter repo: the architecture and learning surface are implemented, while production hardening remains the next layer.