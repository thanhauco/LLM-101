from __future__ import annotations

from typing import TypedDict, Literal
from langgraph.graph import END, StateGraph


class CRAGState(TypedDict):
    question: str
    documents: list[str]
    needs_web_search: bool
    answer: str


def retrieve_documents(state: CRAGState) -> CRAGState:
    print("-> Node [retrieve_documents]: Retrieving candidates from local index...")
    # Mocking retrieval based on question keywords
    if "transformer" in state["question"].lower():
        state["documents"] = ["The Transformer is a deep learning model introduced in 2017."]
    else:
        state["documents"] = ["Random unrelated reference article about baking bread."]
    return state


def grade_documents(state: CRAGState) -> CRAGState:
    print("-> Node [grade_documents]: Evaluating document relevance...")
    # Grader check: see if question keywords exist in the documents
    relevant_found = False
    for doc in state["documents"]:
        if any(word in doc.lower() for word in ["transformer", "model", "learning"]):
            relevant_found = True
            break
            
    if relevant_found:
        print("   Status: Relevant documents found.")
        state["needs_web_search"] = False
    else:
        print("   Status: Documents are irrelevant. Query correction and web search needed.")
        state["needs_web_search"] = True
    return state


def web_search(state: CRAGState) -> CRAGState:
    print("-> Node [web_search]: Performing web search for missing information...")
    # Add a mock web search document
    state["documents"].append("Web Search Result: RAG (Retrieval-Augmented Generation) optimizes LLM outputs.")
    state["needs_web_search"] = False
    return state


def generate_answer(state: CRAGState) -> CRAGState:
    print("-> Node [generate_answer]: Synthesizing response from gathered context...")
    context_str = "\n".join(state["documents"])
    state["answer"] = f"Generated Answer based on: \n'{context_str}' \nFor question: '{state['question']}'"
    return state


def decide_next_step(state: CRAGState) -> Literal["web_search", "generate"]:
    if state["needs_web_search"]:
        return "web_search"
    return "generate"


def build_crag_graph():
    workflow = StateGraph(CRAGState)
    
    # Add all nodes
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("grade", grade_documents)
    workflow.add_node("web_search", web_search)
    workflow.add_node("generate", generate_answer)
    
    # Establish connection flow
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade")
    
    # Add conditional route based on grading result
    workflow.add_conditional_edges(
        "grade",
        decide_next_step,
        {
            "web_search": "web_search",
            "generate": "generate"
        }
    )
    
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()


if __name__ == "__main__":
    print("=== LLMs 101: Corrective RAG (CRAG) with LangGraph ===")
    graph = build_crag_graph()
    
    print("\n--- Test Scenario 1: Relevant Docs Match ---")
    res1 = graph.invoke({"question": "Explain the Transformer model", "documents": [], "needs_web_search": False, "answer": ""})
    print("\nResult 1:")
    print(res1["answer"])
    
    print("\n--- Test Scenario 2: Irrelevant Docs (Fallback triggered) ---")
    res2 = graph.invoke({"question": "What is RAG?", "documents": [], "needs_web_search": False, "answer": ""})
    print("\nResult 2:")
    print(res2["answer"])
