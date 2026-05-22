export type ChatMessage = {
  role: "system" | "user" | "assistant";
  content: string;
};

export type ChatResponse = {
  model: string;
  content: string;
  usage?: Record<string, unknown>;
};

export async function sendChat(messages: ChatMessage[], model?: string): Promise<ChatResponse> {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages, model, temperature: 0.2, max_tokens: 512 })
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || "Chat request failed");
  }

  return response.json() as Promise<ChatResponse>;
}

export async function getRoute(task: string, contextTokens: number) {
  const params = new URLSearchParams({ task, context_tokens: String(contextTokens) });
  const response = await fetch(`/api/models/route?${params.toString()}`);
  if (!response.ok) {
    throw new Error("Model routing request failed");
  }
  return response.json() as Promise<{ model: string; reason: string; max_context_tokens: number }>;
}
