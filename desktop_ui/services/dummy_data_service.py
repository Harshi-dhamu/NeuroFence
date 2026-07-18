"""Realistic temporary provider used until teammate APIs are frozen."""
from __future__ import annotations

from itertools import cycle
from pathlib import Path

from desktop_ui.models.model_metadata import ModelMetadata
from desktop_ui.models.scan_result import (
    ActivationResults,
    DetectionResults,
    ScanResult,
    ScanStatistics,
)


class DummyDataService:
    """Produce complete ScanResult objects through the future backend contract."""

    _PROFILES = cycle((
        {"name": "TinyLlama", "framework": "PyTorch", "architecture": "Transformer", "layers": 22,
         "size": 1100.0, "score": 18, "risk": "LOW", "dead": 7, "duration": 4.1},
        {"name": "Mistral-7B", "framework": "PyTorch", "architecture": "Mistral Transformer", "layers": 32,
         "size": 13800.0, "score": 34, "risk": "MEDIUM", "dead": 18, "duration": 6.8},
        {"name": "DeepSeek-R1-Distill", "framework": "Safetensors", "architecture": "Decoder Transformer", "layers": 28,
         "size": 8500.0, "score": 11, "risk": "LOW", "dead": 4, "duration": 5.5},
        {"name": "Phi-3-mini", "framework": "ONNX", "architecture": "Phi Transformer", "layers": 32,
         "size": 7200.0, "score": 72, "risk": "HIGH", "dead": 41, "duration": 7.3},
    ))

    def get_scan_result(self, model_path: str = "") -> ScanResult:
        profile = dict(next(self._PROFILES))
        selected_name = Path(model_path).name if model_path else ""
        if selected_name:
            profile["name"] = selected_name

        score = int(profile["score"])
        risk = str(profile["risk"])
        safe = score < 60
        status = "SAFE" if safe else "SUSPICIOUS"

        model = ModelMetadata(
            model_name=str(profile["name"]), model_path=model_path,
            framework=str(profile["framework"]), architecture=str(profile["architecture"]),
            file_size_mb=float(profile["size"]), layers=int(profile["layers"]),
            parameters="3.8B" if "Phi" in str(profile["name"]) else "7B",
        )
        detection = DetectionResults(
            threat_score=score, risk_level=risk,
            suspicious_prompts=[] if safe else ["Hidden trigger phrase pattern"],
            suspicious_weight_count=0 if safe else 3,
            summary=("No confirmed poisoned weights or backdoor triggers detected."
                     if safe else "Potential backdoor indicators require analyst review."),
        )
        activation = ActivationResults(
            neurons_analyzed=12480, dead_neurons=int(profile["dead"]),
            anomalous_activations=0 if safe else 6,
            summary=("Activation patterns remain within the expected baseline range."
                     if safe else "Several activation clusters deviate from the baseline."),
            neuron_information={"peak_activation": 0.82 if safe else 0.97, "mean_activation": 0.31},
        )
        statistics = ScanStatistics(
            duration_seconds=float(profile["duration"]), overall_status=status, stages_completed=9
        )
        recommendation = (
            "No suspicious behaviour detected. Continue routine monitoring."
            if safe else "Quarantine the model and perform a deeper manual investigation before deployment."
        )
        return ScanResult(
            model=model, detection=detection, activation=activation,
            statistics=statistics, recommendation=recommendation,
            metadata={"provider": "DummyDataService", "data_driven": True},
        )
