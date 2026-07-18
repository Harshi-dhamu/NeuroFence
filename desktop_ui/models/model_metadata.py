"""Model metadata contract shared by the UI and backend services."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ModelMetadata:
    model_name: str = "Unknown Model"
    model_path: str = ""
    framework: str = "Unknown"
    architecture: str = "Unknown"
    file_size_mb: float = 0.0
    layers: int = 0
    parameters: str = "Unknown"
    source: str = "DummyDataService"
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
