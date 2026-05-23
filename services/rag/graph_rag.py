from __future__ import annotations

class SimpleGraphRAG:
    """A pedagogical, pure-Python implementation of GraphRAG concepts.
    Shows how entities and relations form a knowledge graph to answer global context queries.
    """
    def __init__(self):
        # Nodes: entity -> description
        self.nodes: dict[str, str] = {}
        # Edges: (entity_a, entity_b) -> relationship description
        self.edges: dict[tuple[str, str], str] = {}

    def add_entity(self, name: str, description: str):
        self.nodes[name.lower()] = description

    def add_relation(self, source: str, target: str, relationship: str):
        self.edges[(source.lower(), target.lower())] = relationship

    def query(self, user_query: str) -> str:
        # 1. Identify which entities are mentioned in the query
        matched_entities = []
        for entity in self.nodes:
            if entity in user_query.lower():
                matched_entities.append(entity)
                
        if not matched_entities:
            return "No entities matching the query were found in the Knowledge Graph."

        # 2. Extract facts about matching entities
        retrieved_facts = []
        retrieved_facts.append("=== Matching Entities ===")
        for entity in matched_entities:
            retrieved_facts.append(f"- {entity.upper()}: {self.nodes[entity]}")

        # 3. Retrieve relationships connected to these entities
        retrieved_facts.append("\n=== Connected Relations ===")
        found_relations = False
        for (src, tgt), rel in self.edges.items():
            if src in matched_entities or tgt in matched_entities:
                retrieved_facts.append(f"- {src.upper()} --({rel})--> {tgt.upper()}")
                found_relations = True
                
        if not found_relations:
            retrieved_facts.append("- No direct relationships found.")

        # 4. Formulate the LLM prompt context
        context = "\n".join(retrieved_facts)
        
        # Simulated LLM generation block (in production, we pass context to the OpenAI client)
        response = (
            f"GraphRAG Synthesized Response:\n"
            f"Based on the Knowledge Graph context:\n"
            f"  - We resolved query target entities: {', '.join(e.upper() for e in matched_entities)}\n"
            f"  - Relationships explain that: "
        )
        
        rel_explanations = []
        for (src, tgt), rel in self.edges.items():
            if src in matched_entities or tgt in matched_entities:
                rel_explanations.append(f"{src.upper()} is linked to {tgt.upper()} via '{rel}'")
        response += ", and ".join(rel_explanations) + "."
        
        return f"--- Retrieved Subgraph Context ---\n{context}\n\n--- Answer ---\n{response}"


if __name__ == "__main__":
    print("=== LLMs 101: GraphRAG (Entity-Relation RAG) Demo ===")
    
    # Initialize the Graph Database
    kg = SimpleGraphRAG()
    
    # Index some entities
    kg.add_entity("vLLM", "An engine designed for high-throughput LLM serving via PagedAttention.")
    kg.add_entity("PagedAttention", "A memory management algorithm that reduces KV Cache fragmentation.")
    kg.add_entity("KV Cache", "An optimization caching attention vectors to speed up LLM token generation.")
    kg.add_entity("speculative decoding", "An execution model where a small draft model verifies tokens with a target model.")
    
    # Establish relationships
    kg.add_relation("vLLM", "PagedAttention", "uses to manage memory")
    kg.add_relation("PagedAttention", "KV Cache", "optimizes storage of")
    kg.add_relation("vLLM", "speculative decoding", "supports to accelerate serving")

    # Run queries
    print("\nQuery 1: Tell me about PagedAttention and how it fits into serving.")
    result1 = kg.query("Tell me about PagedAttention and what it affects")
    print(result1)
    
    print("\n" + "="*50)
    print("\nQuery 2: Explain KV Cache and vLLM")
    result2 = kg.query("Explain KV Cache and vLLM")
    print(result2)
