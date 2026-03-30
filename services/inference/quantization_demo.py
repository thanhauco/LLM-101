from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuantizationProfile:
    name: str
    bits: int
    memory_ratio: float
    best_for: str
    tradeoff: str


PROFILES = [
    QuantizationProfile("fp16", 16, 1.0, "baseline GPU inference", "highest memory use"),
    QuantizationProfile("int8", 8, 0.5, "balanced serving", "small quality and speed tradeoffs"),
    QuantizationProfile("nf4", 4, 0.25, "QLoRA and constrained GPUs", "training and kernel support matter"),
    QuantizationProfile("gguf-q4_k_m", 4, 0.28, "llama.cpp CPU or edge serving", "model-specific quality variance"),
]


def estimate_model_memory(parameters_billions: float, profile: QuantizationProfile) -> float:
    fp16_gb = parameters_billions * 2
    return fp16_gb * profile.memory_ratio


def main() -> None:
    parameters_billions = 7
    print("profile,bits,estimated_gb,best_for,tradeoff")
    for profile in PROFILES:
        memory_gb = estimate_model_memory(parameters_billions, profile)
        print(
            f"{profile.name},{profile.bits},{memory_gb:.2f},"
            f"{profile.best_for},{profile.tradeoff}"
        )


if __name__ == "__main__":
    main()
