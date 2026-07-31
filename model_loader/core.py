"""
model_loader/core.py
Provides core functionality for model validation, sandboxing, memory projection,
and metadata export features for NeuroFence.
"""

import json
import os
from typing import Any, Dict, Optional


def check_directory_exists(path: str) -> bool:
    """Helper function to check if a directory exists."""
    return os.path.exists(path) and os.path.isdir(path)


class SandboxEnvironment:
    """Mock/Stub sandbox environment used for staging model loading safely."""

    def __init__(self, target_path: Optional[str] = None):
        self.target_path = target_path

    def initialize_sandbox(self) -> bool:
        return True

    def execute_safely(self) -> bool:
        return True

    def run(self, action: str = "load") -> bool:
        return True


def calculate_memory_projection(
    param_count: float, precision: str = "float16", overhead_factor: float = 1.2
) -> Dict[str, Any]:
    """Calculates estimated RAM/VRAM required to load an AI model.

    :param param_count: Total parameter count (in billions or raw count).
    :param precision: Precision format ('float32', 'float16', 'bfloat16', 'int8',
      'int4').
    :param overhead_factor: Safety buffer factor for KV-cache and overhead
      (default 1.2).
    :return: Dictionary containing calculated memory projections.
    """
    bytes_per_param_map = {
        "float32": 4.0,
        "fp32": 4.0,
        "float16": 2.0,
        "fp16": 2.0,
        "bfloat16": 2.0,
        "bf16": 2.0,
        "int8": 1.0,
        "q8": 1.0,
        "int4": 0.5,
        "q4": 0.5,
    }

    precision_clean = str(precision).strip().lower()
    bytes_per_param = bytes_per_param_map.get(precision_clean, 2.0)
    actual_params = param_count * 1e9 if param_count < 1000 else param_count

    base_memory_bytes = actual_params * bytes_per_param
    total_memory_bytes = base_memory_bytes * overhead_factor

    base_gb = base_memory_bytes / (1024**3)
    total_gb = total_memory_bytes / (1024**3)
    total_mb = total_memory_bytes / (1024**2)

    return {
        "param_count": param_count,
        "precision": precision_clean,
        "bytes_per_param": bytes_per_param,
        "base_weight_gb": round(base_gb, 2),
        "estimated_total_gb": round(total_gb, 2),
        "estimated_total_mb": round(total_mb, 2),
    }


class ModelLoader:

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.is_validated: bool = False
        self.metadata: Dict[str, Any] = {
            "raw_config": {},
            "status": "uninitialized",
            "param_count": 0.0,
            "verification_report": {"config_verified": False},
        }

    def scan_model_directory(self, path: Optional[str] = None) -> bool:
        """Scans and validates existence of target model directory."""
        target_path = path or self.model_path
        if not target_path or not check_directory_exists(target_path):
            self.is_validated = False
            return False
        self.is_validated = True
        return True

    def scan_directory(self, path: Optional[str] = None) -> bool:
        """Alias for scan_model_directory."""
        return self.scan_model_directory(path)

    def verify_config_keys(self, required_keys: Optional[list] = None) -> bool:
        """Verifies presence of required architectural parameters in config."""
        raw_cfg = self.metadata.get("raw_config", {})
        if required_keys is None:
            required_keys = ["hidden_size", "num_hidden_layers", "vocab_size"]

        is_valid = bool(raw_cfg) and all(k in raw_cfg for k in required_keys)
        if "verification_report" not in self.metadata:
            self.metadata["verification_report"] = {}
        self.metadata["verification_report"]["config_verified"] = is_valid
        return is_valid

    def estimate_parameter_count(self) -> float:
        """Estimates model parameter count based on architectural configurations."""
        cfg = self.metadata.get("raw_config", {})
        hidden_size = cfg.get("hidden_size", 4096)
        num_layers = cfg.get("num_hidden_layers", 32)
        vocab_size = cfg.get("vocab_size", 32000)
        intermediate_size = cfg.get("intermediate_size", 11008)

        attn_params = 4 * (hidden_size**2)
        mlp_params = 3 * hidden_size * intermediate_size
        embed_params = vocab_size * hidden_size

        raw_estimated = (num_layers * (attn_params + mlp_params)) + embed_params
        estimated_in_billions = round(raw_estimated / 1e9, 2)
        self.metadata["param_count"] = estimated_in_billions
        return estimated_in_billions

    def load_safely(self) -> Dict[str, str]:
        """Safely initializes model in an isolated sandbox environment."""
        try:
            sandbox = SandboxEnvironment(self.model_path)

            if hasattr(sandbox, "initialize_sandbox"):
                sandbox.initialize_sandbox()

            if hasattr(sandbox, "execute_safely"):
                res = sandbox.execute_safely()
            else:
                res = sandbox.run("load")

            if not res or res == "Intercepted" or res == "failed":
                return {"status": "Intercepted"}

            return {"status": "SUCCESS"}
        except Exception as e:
            return {
                "status": "Intercepted",
                "message": "Security runtime failure",
                "error_details": str(e),
            }

    def get_memory_projection(
        self, param_count: Optional[float] = None, precision: str = "float16"
    ) -> Dict[str, Any]:
        """Day 2: Returns RAM/VRAM projection for the target model."""
        if param_count is not None:
            count = param_count
        else:
            count = (
                self.metadata.get("param_count")
                or self.estimate_parameter_count()
            )

        return calculate_memory_projection(
            param_count=count, precision=precision
        )

    def export_metadata(self) -> Dict[str, Any]:
        """Day 3: Exports consolidated model metadata dictionary."""
        projection = self.get_memory_projection()
        return {
            "model_path": self.model_path,
            "is_validated": self.is_validated,
            "param_count_billions": self.metadata.get("param_count", 0),
            "verification_report": self.metadata.get("verification_report", {}),
            "memory_projection": projection,
            "status": self.metadata.get("status", "uninitialized"),
        }

    def export_metadata_to_file(
        self, output_path: str = "model_metadata.json"
    ) -> bool:
        """Day 3: Saves exported metadata dictionary into a formatted JSON file."""
        try:
            data = self.export_metadata()
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error exporting metadata to file: {e}")
            return False