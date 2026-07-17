"""Adapter for Dhruti's Detection & Fuzzing module."""
from __future__ import annotations

import hashlib


class DetectionServiceError(RuntimeError):
    """Raised when detection or fuzzing cannot complete."""


class DetectionService:
    """Run placeholder weight analysis and adversarial prompt tests."""

    def run_detection(self, model_info: dict[str, object]) -> dict[str, object]:
        model_name = str(model_info.get("model_name", ""))
        if not model_name:
            raise DetectionServiceError("Detection did not receive valid model metadata.")

        # Deterministic demonstration output keeps repeated scans predictable.
        digest = hashlib.sha256(model_name.encode("utf-8")).digest()
        threat_score = 8 + digest[0] % 24
        risk_level = "LOW" if threat_score < 30 else "MEDIUM"

        # TODO(Dhruti): replace with the real Detection & Fuzzing engine.
        return {
            "threat_score": threat_score,
            "risk_level": risk_level,
            "suspicious_prompts": [],
            "suspicious_weight_count": 0,
            "detection_summary": "No confirmed poisoned weights or backdoor triggers detected.",
        }
