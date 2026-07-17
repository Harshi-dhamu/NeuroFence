"""Communication bridge between NeuroFence UI and backend modules."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from desktop_ui.services.activation_service import ActivationService
from desktop_ui.services.detection_service import DetectionService
from desktop_ui.services.model_service import ModelService


@dataclass(slots=True)
class ScanResult:
    """Common result contract contributed to by every backend module."""

    model_name: str = "Unknown Model"
    model_path: str = ""
    framework: str = "Unknown"
    architecture: str = "Unknown"
    file_size_mb: float = 0.0
    layers: int = 0
    threat_score: int = 0
    risk_level: str = "UNKNOWN"
    activation_summary: str = ""
    detection_summary: str = ""
    scan_duration: float = 0.0
    overall_status: str = "UNKNOWN"
    timestamp: str = ""
    suspicious_prompts: list[str] = field(default_factory=list)
    activation_statistics: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    recommendation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class IntegrationBridge:
    """Stable façade that hides teammate-specific module implementations."""

    def __init__(
        self,
        model_service: ModelService | None = None,
        detection_service: DetectionService | None = None,
        activation_service: ActivationService | None = None,
    ) -> None:
        self.model_service = model_service or ModelService()
        self.detection_service = detection_service or DetectionService()
        self.activation_service = activation_service or ActivationService()

    def load_model(self, model_path: str) -> dict[str, object]:
        return self.model_service.load_model(model_path)

    def validate_model(self, model_info: dict[str, object]) -> bool:
        return self.model_service.validate_model(model_info)

    def run_detection(self, model_info: dict[str, object]) -> dict[str, object]:
        return self.detection_service.run_detection(model_info)

    def run_activation_tracker(self, model_info: dict[str, object]) -> dict[str, object]:
        return self.activation_service.run_activation_tracker(model_info)

    def generate_report(
        self,
        model_info: dict[str, object],
        detection: dict[str, object],
        activation: dict[str, object],
        scan_duration: float,
    ) -> ScanResult:
        threat_score = int(detection.get("threat_score", 0))
        status = "SAFE" if threat_score < 30 else "REVIEW"
        recommendation = (
            "No suspicious behaviour detected. Continue routine monitoring."
            if status == "SAFE"
            else "Review the model findings before deployment."
        )
        return ScanResult(
            model_name=str(model_info.get("model_name", "Unknown Model")),
            model_path=str(model_info.get("model_path", "")),
            framework=str(model_info.get("framework", "Unknown")),
            architecture=str(model_info.get("architecture", "Unknown")),
            file_size_mb=float(model_info.get("file_size_mb", 0.0)),
            layers=int(model_info.get("layers", 0)),
            threat_score=threat_score,
            risk_level=str(detection.get("risk_level", "UNKNOWN")),
            activation_summary=str(activation.get("activation_summary", "")),
            detection_summary=str(detection.get("detection_summary", "")),
            scan_duration=scan_duration,
            overall_status=status,
            timestamp=datetime.now().strftime("%d %b %Y, %I:%M %p"),
            suspicious_prompts=list(detection.get("suspicious_prompts", [])),
            activation_statistics=dict(activation),
            metadata=dict(model_info),
            recommendation=recommendation,
        )

    def export_results(self, result: ScanResult, destination: str) -> str:
        # TODO: connect PDF/JSON/CSV report writers in a later sprint.
        return str(Path(destination))
