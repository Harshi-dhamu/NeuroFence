"""Common, data-driven result for one complete NeuroFence scan."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from desktop_ui.models.model_metadata import ModelMetadata


@dataclass(slots=True)
class DetectionResults:
    threat_score: int = 0
    risk_level: str = "UNKNOWN"
    suspicious_prompts: list[str] = field(default_factory=list)
    suspicious_weight_count: int = 0
    summary: str = ""


@dataclass(slots=True)
class ActivationResults:
    neurons_analyzed: int = 0
    dead_neurons: int = 0
    anomalous_activations: int = 0
    summary: str = ""
    neuron_information: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ScanStatistics:
    duration_seconds: float = 0.0
    overall_status: str = "READY"
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%d %b %Y, %I:%M %p"))
    stages_completed: int = 0


@dataclass(slots=True)
class ScanResult:
    model: ModelMetadata = field(default_factory=ModelMetadata)
    detection: DetectionResults = field(default_factory=DetectionResults)
    activation: ActivationResults = field(default_factory=ActivationResults)
    statistics: ScanStatistics = field(default_factory=ScanStatistics)
    metadata: dict[str, Any] = field(default_factory=dict)
    recommendation: str = ""

    # Compatibility properties retained for Day 7/8 pages and integrations.
    @property
    def model_name(self) -> str: return self.model.model_name
    @property
    def model_path(self) -> str: return self.model.model_path
    @property
    def framework(self) -> str: return self.model.framework
    @property
    def architecture(self) -> str: return self.model.architecture
    @property
    def file_size_mb(self) -> float: return self.model.file_size_mb
    @property
    def layers(self) -> int: return self.model.layers
    @property
    def threat_score(self) -> int: return self.detection.threat_score
    @property
    def risk_level(self) -> str: return self.detection.risk_level
    @property
    def detection_summary(self) -> str: return self.detection.summary
    @property
    def activation_summary(self) -> str: return self.activation.summary
    @property
    def activation_statistics(self) -> dict[str, Any]: return self.activation.neuron_information
    @property
    def scan_duration(self) -> float: return self.statistics.duration_seconds
    @property
    def overall_status(self) -> str: return self.statistics.overall_status
    @property
    def timestamp(self) -> str: return self.statistics.timestamp
    @property
    def suspicious_prompts(self) -> list[str]: return self.detection.suspicious_prompts

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
