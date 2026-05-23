from __future__ import annotations

import os
import tempfile
import subprocess
import sys

class PythonCodeSandbox:
    """Safe local subprocess sandboxing for agent code execution."""
    def __init__(self, timeout_seconds: float = 5.0):
        self.timeout = timeout_seconds

    def execute(self, code: str) -> dict[str, str | int]:
        # Create a temporary python file
        fd, path = tempfile.mkstemp(suffix=".py", text=True)
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(code)
            
            # Execute python script in a separate process
            # We restrict environment variables or run in a basic sandbox wrapper in real cases
            # Here we capture stdout/stderr and handle timeouts
            process = subprocess.run(
                [sys.executable, path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            return {
                "stdout": process.stdout,
                "stderr": process.stderr,
                "exit_code": process.returncode,
                "status": "success"
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Execution timed out after {self.timeout} seconds.",
                "exit_code": -1,
                "status": "timeout"
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "exit_code": -2,
                "status": "error"
            }
        finally:
            # Always clean up the temp file
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    print("=== LLMs 101: Agentic Sandboxed Code Interpreter ===")
    sandbox = PythonCodeSandbox(timeout_seconds=2.0)

    # Test 1: Simple valid execution
    valid_code = """
import math
print("Calculating standard deviation...")
data = [10, 12, 23, 23, 16, 23, 21, 16]
mean = sum(data) / len(data)
variance = sum((x - mean) ** 2 for x in data) / len(data)
std_dev = math.sqrt(variance)
print(f"Mean: {mean:.2f}, Std Dev: {std_dev:.2f}")
"""
    print("\nExecuting valid code:")
    res = sandbox.execute(valid_code)
    print(f"Status: {res['status']}")
    print(f"Exit Code: {res['exit_code']}")
    print(f"Stdout:\n{res['stdout']}")
    
    # Test 2: Code with errors
    error_code = """
items = [1, 2, 3]
print(items[10]) # Out of bounds error!
"""
    print("\nExecuting code with errors:")
    res_err = sandbox.execute(error_code)
    print(f"Status: {res_err['status']}")
    print(f"Exit Code: {res_err['exit_code']}")
    print(f"Stderr:\n{res_err['stderr']}")

    # Test 3: Infinite Loop Timeout protection
    loop_code = """
import time
print("Starting infinite loop...")
while True:
    time.sleep(0.1)
"""
    print("\nExecuting infinite loop (testing timeout protection):")
    res_loop = sandbox.execute(loop_code)
    print(f"Status: {res_loop['status']}")
    print(f"Stderr/Timeout Message:\n{res_loop['stderr']}")
