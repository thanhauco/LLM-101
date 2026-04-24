from __future__ import annotations

from pathlib import Path


def collect_repo_context(root: str | Path, patterns: tuple[str, ...] = ("*.py", "*.ts", "*.tsx")) -> str:
    root_path = Path(root)
    snippets: list[str] = []
    for pattern in patterns:
        for path in root_path.rglob(pattern):
            if any(part in {"node_modules", ".venv", ".next"} for part in path.parts):
                continue
            snippets.append(f"# {path}\n{path.read_text(encoding='utf-8', errors='ignore')[:4000]}")
    return "\n\n".join(snippets)


def generate_patch_prompt(diff_context: str) -> str:
    return f"""
Return a focused patch that fixes the bug. Include tests only when the behavior needs coverage.

Diff and context:
{diff_context}
""".strip()
