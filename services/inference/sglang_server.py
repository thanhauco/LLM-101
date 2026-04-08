from __future__ import annotations

import os
import subprocess


def build_sglang_command() -> list[str]:
    return [
        "python",
        "-m",
        "sglang.launch_server",
        "--model-path",
        os.getenv("SGLANG_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        "--host",
        os.getenv("SGLANG_HOST", "0.0.0.0"),
        "--port",
        os.getenv("SGLANG_PORT", "8002"),
    ]


def main() -> None:
    subprocess.run(build_sglang_command(), check=True)


if __name__ == "__main__":
    main()