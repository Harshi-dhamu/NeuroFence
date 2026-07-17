"""Adapter for Tanvi's Model Loader & Sandbox module."""
from __future__ import annotations

from pathlib import Path


class ModelServiceError(RuntimeError):
    """Raised when model loading or validation fails."""


class ModelService:
    """Load a model and return normalized metadata for the scan pipeline."""

    def load_model(self, model_path: str) -> dict[str, object]:
        path = Path(model_path)
        if not model_path:
            raise ModelServiceError("No model was selected.")
        if not path.exists():
            raise ModelServiceError(f"The selected model path does not exist: {model_path}")

        model_files = [item for item in path.rglob("*") if item.is_file()] if path.is_dir() else [path]
        total_bytes = sum(item.stat().st_size for item in model_files if item.exists())
        suffixes = {item.suffix.lower() for item in model_files}

        framework = "PyTorch"
        if ".h5" in suffixes or ".keras" in suffixes:
            framework = "TensorFlow / Keras"
        elif ".onnx" in suffixes:
            framework = "ONNX"
        elif ".gguf" in suffixes:
            framework = "GGUF"

        # TODO(Tanvi): replace this placeholder inspection with the real
        # Model Loader & Sandbox API while preserving this return structure.
        return {
            "model_name": path.name or "Selected Model",
            "model_path": str(path),
            "framework": framework,
            "architecture": "Transformer (placeholder)",
            "file_size_mb": round(total_bytes / (1024 * 1024), 2),
            "layers": 24,
            "file_count": len(model_files),
        }

    def validate_model(self, metadata: dict[str, object]) -> bool:
        # TODO(Tanvi): perform sandbox validation, format checks and integrity
        # verification here. Raise ModelServiceError for friendly UI handling.
        if not metadata.get("model_name"):
            raise ModelServiceError("Model metadata is incomplete.")
        return True
