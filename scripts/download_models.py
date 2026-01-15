from __future__ import annotations

from huggingface_hub import snapshot_download


def download_model(model_id: str, local_dir: str) -> None:
    snapshot_download(repo_id=model_id, local_dir=local_dir, local_dir_use_symlinks=False)


if __name__ == "__main__":
    download_model("Qwen/Qwen2.5-7B-Instruct", "models/safetensors/qwen2.5-7b-instruct")
