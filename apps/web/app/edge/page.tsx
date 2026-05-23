"use client";

import { useState } from "react";
import { Cpu, Send, Sparkles, ShieldCheck, ArrowLeft, Bot, Database, Download } from "lucide-react";
import Link from "next/link";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

export default function EdgePage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "assistant", content: "Edge AI console ready. You can simulate running a model in the browser using WebGPU." }
  ]);
  const [input, setInput] = useState("");
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [isDownloading, setIsDownloading] = useState(false);
  const [isModelLoaded, setIsModelLoaded] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const startDownloadSim = () => {
    setIsDownloading(true);
    setDownloadProgress(0);
    const interval = setInterval(() => {
      setDownloadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsDownloading(false);
          setIsModelLoaded(true);
          setMessages((msgs) => [
            ...msgs,
            { role: "assistant", content: "Model 'Qwen-1.5-0.5B-Chat' successfully loaded into WebGPU VRAM. Ready for private offline chat!" }
          ]);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isGenerating) return;

    if (!isModelLoaded) {
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant", content: "Please load the model into your browser memory (VRAM) first before sending messages." }
      ]);
      setInput("");
      return;
    }

    const nextMessages: ChatMessage[] = [...messages, { role: "user", content: input }];
    setMessages(nextMessages);
    setInput("");
    setIsGenerating(true);

    // Simulate WebGPU token generation
    setTimeout(() => {
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant", content: "This is a local inference response generated directly in your browser using WebGPU. No network requests were sent!" }
      ]);
      setIsGenerating(false);
    }, 1200);
  };

  return (
    <main className="shell">
      <aside className="rail" aria-label="Primary">
        <div className="brand">
          <span className="brandMark">L</span>
          <span>LLMs 101</span>
        </div>
        <nav className="navList">
          <Link href="/"><ArrowLeft size={18} /> Back to main</Link>
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar animatedEntry">
          <div>
            <p className="eyebrow">Client-side Compute</p>
            <h1>Browser Edge Inference</h1>
          </div>
          <div className="healthStrip" aria-label="Edge status">
            <span><Cpu size={16} /> WebGPU Supported</span>
            <span><ShieldCheck size={16} /> 100% Private & Offline</span>
          </div>
        </header>

        <section className="statusGrid">
          <article className="statusTile animatedEntry" style={{ animationDelay: "80ms" }}>
            <div className="tileIcon"><Cpu size={19} /></div>
            <div>
              <p>Model Status</p>
              <strong>{isModelLoaded ? "Loaded in VRAM" : "Not Loaded"}</strong>
            </div>
            <span className={`status ${isModelLoaded ? "ready" : "idle"}`}>
              {isModelLoaded ? "ready" : "pending"}
            </span>
          </article>
          <article className="statusTile animatedEntry" style={{ animationDelay: "160ms" }}>
            <div className="tileIcon"><Database size={19} /></div>
            <div>
              <p>Model Spec</p>
              <strong>Qwen-0.5B (GGUF/WASM)</strong>
            </div>
            <span className="status ready">0.5B params</span>
          </article>
        </section>

        <section className="mainGrid">
          <section className="chatPanel animatedEntry" style={{ animationDelay: "240ms" }}>
            <div className="panelHeader">
              <div>
                <p className="eyebrow">Interactive Console</p>
                <h2>Transformers.js Local Sandbox</h2>
              </div>
              {!isModelLoaded && !isDownloading && (
                <button className="modelPicker" style={{ display: "flex", gap: "8px", alignItems: "center", cursor: "pointer", background: "none" }} onClick={startDownloadSim}>
                  <Download size={16} /> Load Model
                </button>
              )}
              {isDownloading && (
                <div style={{ fontSize: "0.85rem", color: "var(--muted)" }}>
                  Downloading Model: {downloadProgress}%
                </div>
              )}
            </div>

            <div className="messages">
              {messages.map((message, index) => (
                <div className={`message ${message.role}`} key={`${message.role}-${index}`}>
                  <span>{message.role === "user" ? "user (local)" : "assistant (webgpu)"}</span>
                  <p>{message.content}</p>
                </div>
              ))}
              {isGenerating && <div className="typing"><i /><i /><i /></div>}
            </div>

            <form className="composer" onSubmit={handleSend}>
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={isModelLoaded ? "Message local model..." : "Please load model first..."}
                rows={2}
                disabled={!isModelLoaded || isGenerating}
                aria-label="Message"
              />
              <button type="submit" disabled={!isModelLoaded || isGenerating} aria-label="Send message" title="Send message">
                <Send size={18} />
              </button>
            </form>
          </section>

          <aside className="sideStack">
            <section className="panel">
              <div className="panelHeader compact">
                <h2>Edge Architecture</h2>
                <Sparkles size={18} />
              </div>
              <div className="feedList">
                <p style={{ fontSize: "0.85rem", lineHeight: "1.4", margin: 0, color: "var(--muted)" }}>
                  WebGPU allows browser-based applications to access the user&apos;s physical GPU hardware directly. 
                  By loading quantized model weights into browser VRAM via ONNX Runtime or WebLLM, you achieve:
                </p>
                <ul style={{ fontSize: "0.82rem", color: "var(--muted)", margin: "8px 0 0 16px", padding: 0 }}>
                  <li>Complete offline usage (works on an airplane)</li>
                  <li>Zero server host cost</li>
                  <li>Strict privacy compliance (no user prompts leave the machine)</li>
                </ul>
              </div>
            </section>
          </aside>
        </section>
      </section>
    </main>
  );
}
