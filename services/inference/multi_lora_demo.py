from __future__ import annotations

import json

def explain_multi_lora():
    print("=== LLMs 101: Multi-LoRA Dynamic Serving ===")
    print("This demo explains how a single base LLM serves multiple task-specific LoRA adapters dynamically.\n")
    
    print("1. How it works:")
    print("   - The base model (e.g. Llama-3-8B) is loaded into GPU memory once.")
    print("   - Several lightweight LoRA adapters (e.g. math-expert, sql-coder, translator) are stored on disk.")
    print("   - During a request, you specify which adapter to load. The model runner dynamically overlays the ")
    print("     adapter weights onto the base model attention matrices for that specific batch request.")
    print("-" * 60)
    
    # Showcase vLLM request format
    print("\n2. vLLM Multi-LoRA API Request Payload Structure:")
    
    math_request = {
        "model": "llama-3-base",
        "messages": [{"role": "user", "content": "Calculate the derivative of x^2 + 5x."}],
        "lora_request": {
            "lora_name": "math-expert",
            "local_lora_path": "/models/loras/math-expert-adapter"
        }
    }
    
    sql_request = {
        "model": "llama-3-base",
        "messages": [{"role": "user", "content": "Find all users registered in the last 24h."}],
        "lora_request": {
            "lora_name": "sql-coder",
            "local_lora_path": "/models/loras/sql-coder-adapter"
        }
    }
    
    print("\n--- Math Adapter Request Payload ---")
    print(json.dumps(math_request, indent=2))
    
    print("\n--- SQL Adapter Request Payload ---")
    print(json.dumps(sql_request, indent=2))
    print("-" * 60)
    
    # Explain how to start vLLM with LoRA enabled
    print("\n3. Starting vLLM with LoRA Enabled:")
    print("To enable multi-LoRA serving in your vLLM docker deployment, run:")
    print("  python -m vllm.entrypoints.openai.api_server \\")
    print("    --model meta-llama/Meta-Llama-3-8B-Instruct \\")
    print("    --enable-lora \\")
    print("    --max-loras 4 \\")
    print("    --max-lora-rank 16")
    print("\nThis allows the GPU runtime to hot-swap up to 4 different adapters on the fly!")

if __name__ == "__main__":
    explain_multi_lora()
