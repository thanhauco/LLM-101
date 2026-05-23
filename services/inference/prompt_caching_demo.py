from __future__ import annotations

import time
import requests

def mock_prompt_caching_simulation():
    """Simulates prompt caching performance improvements to demonstrate the concept without a GPU."""
    print("--- Simulating Prompt Caching Prefill Latency ---")
    
    # Large context text block (e.g., an entire reference book or document)
    large_context = "System Instructions:\n" + ("This is reference knowledge line. " * 3000)
    user_prompt_1 = "\nQuery 1: What is the main subject?"
    user_prompt_2 = "\nQuery 2: Summarize the document."
    
    print(f"Large Context Size: {len(large_context.split())} tokens (approximate)")
    print("\n[Run 1] Cache Miss (First run - full prefill needed):")
    print("Sending Large Context + Query 1...")
    
    # Simulating standard prefill latency (approx 50ms per 1000 tokens)
    start_time = time.time()
    time.sleep(1.5)  # Simulated prefill calculation delay
    time.sleep(0.3)  # Simulated generation delay
    duration_miss = time.time() - start_time
    print(f"Time to First Token (TTFT): 1.50 seconds")
    print(f"Total Response Time: {duration_miss:.2f} seconds")
    print("Output: The subject is reference knowledge.")
    
    print("\n[Run 2] Cache Hit (Second run - exact same context prefix reused):")
    print("Sending Large Context + Query 2...")
    
    start_time = time.time()
    time.sleep(0.05) # Simulated prefill (cache hit - negligible delay)
    time.sleep(0.35) # Simulated generation delay
    duration_hit = time.time() - start_time
    print(f"Time to First Token (TTFT): 0.05 seconds (Cache Hit!)")
    print(f"Total Response Time: {duration_hit:.2f} seconds")
    print("Output: Summary of reference knowledge.")
    
    speedup = (1.50 / 0.05)
    print(f"\nPrompt Caching Result: {speedup:.1f}x reduction in Time to First Token (TTFT)!")

def check_local_server_caching():
    """Demonstrates how to fetch with actual caching headers on a vLLM/SGLang local server if online."""
    print("\nFor vLLM and SGLang (vLLM has automatic block-level prefix caching enabled via --enable-prefix-caching):")
    example_payload = {
        "model": "qwen-local",
        "prompt": "Context: [large text...] Query: hello",
        "temperature": 0.0,
        "max_tokens": 10
    }
    print("To run with Prefix Caching in Docker Compose, execute:")
    print("  docker run -d --gpus all -v ~/.cache/huggingface:/root/.cache/huggingface -p 8000:8000 \\")
    print("    vllm/vllm-openai:latest --model Qwen/Qwen2.5-7B-Instruct --enable-prefix-caching\n")
    print("No additional payload flags are required! vLLM handles prefix matching dynamically in its KV cache manager.")

if __name__ == "__main__":
    print("=== LLMs 101: Context Caching & Prompt Caching Demo ===")
    mock_prompt_caching_simulation()
    check_local_server_caching()
