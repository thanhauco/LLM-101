from __future__ import annotations

import os
from pathlib import Path

from paddleocr import PaddleOCR
from transformers import AutoProcessor


def load_vl_processor(model_name: str | None = None):
    return AutoProcessor.from_pretrained(model_name or os.getenv("VL_MODEL", "Qwen/Qwen2.5-VL-7B-Instruct"))


def extract_text_with_ocr(image_path: str | Path) -> str:
    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    result = ocr.ocr(str(image_path), cls=True)
    lines = [line[1][0] for page in result for line in page]
    return "\n".join(lines)
