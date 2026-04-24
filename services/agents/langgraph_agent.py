from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph


class AgentState(TypedDict):
    question: str
    context: list[str]
    answer: str


def retrieve_docs(state: AgentState) -> AgentState:
    state["context"] = ["Retrieved context placeholder for: " + state["question"]]
    return state


def generate_answer(state: AgentState) -> AgentState:
    state["answer"] = "Use the retrieved context to answer: " + state["question"]
    return state


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("retrieve", retrieve_docs)
    graph.add_node("generate", generate_answer)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    print(app.invoke({"question": "What makes RAG fail?", "context": [], "answer": ""}))
