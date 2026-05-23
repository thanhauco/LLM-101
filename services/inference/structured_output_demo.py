from __future__ import annotations

import json
from typing import Literal
from pydantic import BaseModel, Field


class DatabaseQuery(BaseModel):
    """Pydantic model representing a structured SQL database query extraction."""
    table: Literal["users", "orders", "products"] = Field(..., description="The database table to query")
    columns: list[str] = Field(..., description="List of columns to retrieve")
    filters: list[str] = Field(default_factory=list, description="Filter conditions, e.g., ['status = active']")
    limit: int = Field(default=10, description="Max rows to return")


def main():
    print("=== LLMs 101: Structured Outputs & Guided Decoding ===")
    print("This demo showcases how to force an LLM output to conform to a Pydantic schema.\n")
    
    # 1. Inspect the Pydantic Schema that we want to enforce
    schema = DatabaseQuery.model_json_schema()
    print("Target JSON Schema to enforce:")
    print(json.dumps(schema, indent=2))
    print("-" * 50)
    
    # 2. Showcase how we format this for various serving frameworks:
    # - vLLM and SGLang accept guided decoding options
    print("\nFor vLLM and SGLang Serving:")
    vllm_request_payload = {
        "model": "qwen-local",
        "messages": [{"role": "user", "content": "Fetch active orders limit 5"}],
        "guided_json": schema  # Enforces schema at the logit level during decoding!
    }
    print("vLLM Guided JSON Request Payload:")
    print(json.dumps(vllm_request_payload, indent=2))
    
    # - OpenAI compatible API gateway
    print("\nFor OpenAI / FastAPI Gateway:")
    openai_request_payload = {
        "model": "qwen-local",
        "messages": [{"role": "user", "content": "Fetch active orders limit 5"}],
        "response_format": {
            "type": "json_object",
            "schema": schema
        }
    }
    print("OpenAI/FastAPI Response Format Payload:")
    print(json.dumps(openai_request_payload, indent=2))
    print("-" * 50)

    # 3. Local/Mock constraint demonstration (pedagogical fallback)
    raw_unstructured_output = """
    Sure, here is the query representation. 
    We should retrieve columns 'id', 'user_id', and 'total' from the orders table.
    We only want orders that are completed, and let's get the top 5 records.
    {
        "table": "orders",
        "columns": ["id", "user_id", "total"],
        "filters": ["status = 'completed'"],
        "limit": 5
    }
    """
    
    print("\nLocal Fallback Parsing and Validation:")
    print("Raw unstructured LLM output:")
    print(raw_unstructured_output)
    
    # Simple JSON extraction logic (how a gateway handles it if guided decoding is not supported natively)
    try:
        # Find the JSON boundaries
        start_idx = raw_unstructured_output.find("{")
        end_idx = raw_unstructured_output.rfind("}") + 1
        json_str = raw_unstructured_output[start_idx:end_idx]
        
        parsed_data = json.loads(json_str)
        # Validate using Pydantic
        query_object = DatabaseQuery(**parsed_data)
        
        print("\nSuccessfully Parsed & Validated Pydantic Object:")
        print(f"Table:   {query_object.table}")
        print(f"Columns: {query_object.columns}")
        print(f"Filters: {query_object.filters}")
        print(f"Limit:   {query_object.limit}")
    except Exception as e:
        print(f"Validation failed: {e}")

if __name__ == "__main__":
    main()
