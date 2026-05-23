"use client";

import {
  Activity,
  Bot,
  Braces,
  Cpu,
  Database,
  FileSearch,
  Gauge,
  GitBranch,
  Play,
  Radio,
  Route,
  Send,
  ShieldCheck,
  Sparkles,
  Workflow
} from "lucide-react";
import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { D3MetricsChart } from "@/components/D3MetricsChart";
import { D3SystemMap } from "@/components/D3SystemMap";
import { ChatMessage, getRoute, sendChat } from "@/lib/api";
import Link from "next/link";

const systemMessage: ChatMessage = {
  role: "system",
  content: "You are a concise local LLM systems assistant."
};

const pipelines = [
  { label: "Inference", value: "vLLM", icon: Bot, status: "ready" },
  { label: "Retrieval", value: "Qdrant", icon: Database, status: "idle" },
  { label: "Rerank", value: "BGE", icon: FileSearch, status: "idle" },
  { label: "Agents", value: "LangGraph", icon: Workflow, status: "draft" },
  { label: "Evals", value: "Ragas", icon: Braces, status: "queued" },
  { label: "Telemetry", value: "Prometheus", icon: Activity, status: "ready" }
];

const modelRows = [
  { name: "qwen-4b", tier: "small", use: "summaries", latency: "fast" },
  { name: "qwen-local", tier: "medium", use: "chat and RAG", latency: "balanced" },
  { name: "deepseek-coder-local", tier: "medium", use: "coding", latency: "balanced" },
  { name: "qwen-long-context", tier: "large", use: "documents", latency: "slower" }
];

const feedTemplates = [
  "retriever returned 8 candidates from llms101_docs",
  "reranker promoted chunk 3 with score 0.91",
  "router selected qwen-local for chat",
  "token stream 42 tok/s on local endpoint",
  "faithfulness check queued for latest RAG answer",
  "KV cache estimate updated for active conversation",
  "document assistant parsed 12 pages into 38 chunks",
  "Prometheus scrape completed for API metrics"
];

const diagramNodes = ["Prompt", "Router", "Retrieve", "Rerank", "Generate", "Evaluate"];

type FeedItem = {
  id: number;
  text: string;
  kind: "route" | "rag" | "eval" | "metric";
};

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "assistant", content: "Local workbench online. Ask about tokens, RAG, routing, evals, or agents." }
  ]);
  const [input, setInput] = useState("Explain why RAG quality depends on chunking and reranking.");
  const [model, setModel] = useState("");
  const [route, setRoute] = useState<{ model: string; reason: string; max_context_tokens: number } | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [feed, setFeed] = useState<FeedItem[]>(() =>
    feedTemplates.slice(0, 5).map((text, index) => ({
      id: index,
      text,
      kind: ["route", "rag", "eval", "metric", "rag"][index] as FeedItem["kind"]
    }))
  );
  const [pulseIndex, setPulseIndex] = useState(0);
  const feedIdRef = useRef(feedTemplates.length);

  const contextTokens = useMemo(
    () => Math.ceil(messages.map((message) => message.content).join(" ").length / 4),
    [messages]
  );

  useEffect(() => {
    const interval = window.setInterval(() => {
      setPulseIndex((current) => (current + 1) % diagramNodes.length);
      setFeed((items) => {
        const nextId = feedIdRef.current;
        feedIdRef.current += 1;
        const text = feedTemplates[nextId % feedTemplates.length];
        const kinds: FeedItem["kind"][] = ["route", "rag", "eval", "metric"];
        return [{ id: nextId, text, kind: kinds[nextId % kinds.length] }, ...items].slice(0, 7);
      });
    }, 2200);

    return () => window.clearInterval(interval);
  }, []);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || busy) {
      return;
    }

    setBusy(true);
    setError("");
    const nextMessages: ChatMessage[] = [...messages, { role: "user", content: trimmed }];
    setMessages(nextMessages);
    setInput("");

    try {
      const routing = await getRoute("chat", contextTokens);
      setRoute(routing);
      const routeFeedItem: FeedItem = {
        id: feedIdRef.current,
        text: `router selected ${routing.model}`,
        kind: "route"
      };
      feedIdRef.current += 1;
      setFeed((items) => [
        routeFeedItem,
        ...items
      ].slice(0, 7));
      const response = await sendChat(
        [systemMessage, ...nextMessages.filter((message) => message.role !== "assistant")],
        model || undefined
      );
      setMessages([...nextMessages, { role: "assistant", content: response.content }]);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Request failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="shell">
      <aside className="rail" aria-label="Primary">
        <div className="brand">
          <span className="brandMark">L</span>
          <span>LLMs 101</span>
        </div>
        <nav className="navList">
          <a href="#chat"><Bot size={18} /> Chat</a>
          <a href="#rag"><Database size={18} /> RAG</a>
          <a href="#diagram"><Workflow size={18} /> Diagram</a>
          <a href="#feed"><Radio size={18} /> Feed</a>
          <a href="#ops"><Gauge size={18} /> Ops</a>
          <Link href="/edge"><Cpu size={18} /> Edge Compute</Link>
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar animatedEntry">
          <div>
            <p className="eyebrow">Local AI Operating System</p>
            <h1>LLMs 101 Workbench</h1>
          </div>
          <div className="healthStrip" aria-label="Runtime health">
            <span><ShieldCheck size={16} /> API</span>
            <span><Database size={16} /> Qdrant</span>
            <span><Activity size={16} /> Metrics</span>
          </div>
        </header>

        <section className="statusGrid" aria-label="Pipeline status">
          {pipelines.map((item, index) => {
            const Icon = item.icon;
            return (
              <article className="statusTile animatedEntry" style={{ animationDelay: `${index * 80}ms` }} key={item.label}>
                <div className="tileIcon"><Icon size={19} /></div>
                <div>
                  <p>{item.label}</p>
                  <strong>{item.value}</strong>
                </div>
                <span className={`status ${item.status}`}>{item.status}</span>
              </article>
            );
          })}
        </section>

        <section className="mainGrid">
          <section className="chatPanel animatedEntry" id="chat" aria-label="Chat console">
            <div className="panelHeader">
              <div>
                <p className="eyebrow">Chat</p>
                <h2>OpenAI-compatible console</h2>
              </div>
              <label className="modelPicker">
                <Route size={16} />
                <select value={model} onChange={(event) => setModel(event.target.value)} aria-label="Model">
                  <option value="">router default</option>
                  {modelRows.map((row) => (
                    <option key={row.name} value={row.name}>{row.name}</option>
                  ))}
                </select>
              </label>
            </div>

            <div className="messages">
              {messages.map((message, index) => (
                <div className={`message ${message.role}`} key={`${message.role}-${index}`}>
                  <span>{message.role}</span>
                  <p>{message.content}</p>
                </div>
              ))}
              {busy ? <div className="typing"><i /><i /><i /></div> : null}
              {error ? <div className="errorBox">{error}</div> : null}
            </div>

            <form className="composer" onSubmit={submit}>
              <textarea
                value={input}
                onChange={(event) => setInput(event.target.value)}
                rows={3}
                aria-label="Message"
              />
              <button type="submit" disabled={busy} aria-label="Send message" title="Send message">
                {busy ? <Play size={18} /> : <Send size={18} />}
              </button>
            </form>
          </section>

          <aside className="sideStack" aria-label="Runtime panels">
            <section className="panel livePanel" id="feed">
              <div className="panelHeader compact">
                <h2>Live feed</h2>
                <Radio size={18} />
              </div>
              <div className="feedList">
                {feed.map((item) => (
                  <div className={`feedItem ${item.kind}`} key={item.id}>
                    <span />
                    <p>{item.text}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="panel" id="rag">
              <div className="panelHeader compact">
                <h2>Retrieval</h2>
                <Database size={18} />
              </div>
              <dl className="metricList">
                <div><dt>collection</dt><dd>llms101_docs</dd></div>
                <div><dt>top k</dt><dd>8</dd></div>
                <div><dt>rerank k</dt><dd>4</dd></div>
                <div><dt>context</dt><dd>{contextTokens} tokens</dd></div>
              </dl>
            </section>

            <section className="panel" id="ops">
              <div className="panelHeader compact">
                <h2>Model route</h2>
                <GitBranch size={18} />
              </div>
              <dl className="metricList">
                <div><dt>selected</dt><dd>{route?.model ?? "pending"}</dd></div>
                <div><dt>window</dt><dd>{route?.max_context_tokens ?? 32768}</dd></div>
                <div><dt>reason</dt><dd>{route?.reason ?? "default general assistant route"}</dd></div>
              </dl>
            </section>
          </aside>
        </section>

        <section className="diagramPanel animatedEntry" id="diagram" aria-label="Animated AI system diagram">
          <div className="panelHeader compact">
            <h2>Live System Diagram</h2>
            <Sparkles size={18} />
          </div>
          <div className="d3Grid">
            <div className="d3Card">
              <D3SystemMap activeIndex={pulseIndex} />
            </div>
            <div className="d3Card">
              <D3MetricsChart contextTokens={contextTokens} feedCount={feed.length} />
            </div>
          </div>
        </section>

        <section className="modelTable" aria-label="Model catalog">
          <div className="panelHeader compact">
            <h2>Model Catalog</h2>
            <Gauge size={18} />
          </div>
          <div className="table">
            {modelRows.map((row) => (
              <div className="tableRow" key={row.name}>
                <strong>{row.name}</strong>
                <span>{row.tier}</span>
                <span>{row.use}</span>
                <span>{row.latency}</span>
              </div>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}
