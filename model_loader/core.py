"""
model_loader/core.py
Provides core functionality for model validation, sandboxing, memory projection,
metadata export, corrupted model detection, performance tracking, large model
sharding support, validation report export, and metadata caching for NeuroFence.
"""

import copy
import json
import os
import time
from typing import Any, Dict, List, Optional

# Global in-memory cache for model metadata
_METADATA_CACHE: Dict[str, Dict[str, Any]] = {}


def clear_metadata_cache() -> None:
    """Clears the global metadata cache."""
    global _METADATA_CACHE
    _METADATA_CACHE.clear()


def check_directory_exists(path: Optional[str]) -> bool:
    """Helper function to check if a directory exists."""
    return bool(path) and os.path.exists(path) and os.path.isdir(path)


def check_file_corrupted(file_path: str) -> bool:
    """Checks if a model file is corrupted (non-existent, zero-bytes, or unreadable JSON)."""
    if not os.path.exists(file_path):
        return True

    try:
        if os.path.getsize(file_path) == 0:
            return True
    except OSError:
        return True

    if file_path.endswith('.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True

    return False


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
    param_count: Optional[float], 
    precision: str = "float16", 
    overhead_factor: float = 1.2
) -> Dict[str, Any]:
    bytes_per_param_map = {
        "float32": 4.0, "fp32": 4.0,
        "float16": 2.0, "fp16": 2.0,
        "bfloat16": 2.0, "bf16": 2.0,
        "int8": 1.0, "q8": 1.0,
        "int4": 0.5, "q4": 0.5,
    }

    precision_clean = str(precision).strip().lower() if precision else "float16"
    bytes_per_param = bytes_per_param_map.get(precision_clean, 2.0)
    
    count = param_count if param_count is not None else 0.0
    actual_params = count * 1e9 if 0 < count < 1000 else count

    base_memory_bytes = actual_params * bytes_per_param
    total_memory_bytes = base_memory_bytes * overhead_factor

    base_gb = base_memory_bytes / (1024 ** 3)
    total_gb = total_memory_bytes / (1024 ** 3)
    total_mb = total_memory_bytes / (1024 ** 2)

    return {
        "param_count": count,
        "precision": precision_clean,
        "bytes_per_param": bytes_per_param,
        "base_weight_gb": round(base_gb, 2),
        "estimated_total_gb": round(total_gb, 2),
        "estimated_total_mb": round(total_mb, 2),
    }


class ModelLoader:
    def __init__(self, model_path: Optional[str] = None, use_cache: bool = True):
        self.model_path = model_path
        self.use_cache = use_cache
        self.is_validated: bool = False
        self.corrupted_files: List[str] = []
        self.shards: List[str] = []
        self.is_sharded: bool = False
        self.from_cache: bool = False
        self.performance_metrics: Dict[str, float] = {
            "scan_time_ms": 0.0,
            "verification_time_ms": 0.0,
            "load_time_ms": 0.0,
            "total_execution_time_ms": 0.0
        }
        self.metadata: Dict[str, Any] = {
            "raw_config": {},
            "status": "uninitialized",
            "param_count": 0.0,
            "verification_report": {
                "config_verified": False,
                "corruption_detected": False,
                "is_sharded": False
            }
        }

    def detect_model_shards(self, path: Optional[str] = None) -> List[str]:
        target_path = path or self.model_path
        self.shards = []

        if not target_path or not check_directory_exists(target_path):
            self.is_sharded = False
            if "verification_report" in self.metadata:
                self.metadata["verification_report"]["is_sharded"] = False
            return []

        for root, _, files in os.walk(target_path):
            for file in files:
                if "of-" in file.lower() and file.endswith(('.safetensors', '.bin', '.pt', '.gguf')):
                    self.shards.append(file)

        self.is_sharded = len(self.shards) > 0
        if "verification_report" not in self.metadata:
            self.metadata["verification_report"] = {}
        self.metadata["verification_report"]["is_sharded"] = self.is_sharded

        return self.shards

    def detect_corrupted_files(self, path: Optional[str] = None) -> List[str]:
        target_path = path or self.model_path
        self.corrupted_files = []

        if not target_path or not check_directory_exists(target_path):
            if "verification_report" in self.metadata:
                self.metadata["verification_report"]["corruption_detected"] = True
            return []

        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.safetensors', '.bin', '.pt', '.json', '.gguf')):
                    full_path = os.path.join(root, file)
                    if check_file_corrupted(full_path):
                        self.corrupted_files.append(file)

        is_corrupted = len(self.corrupted_files) > 0
        if "verification_report" not in self.metadata:
            self.metadata["verification_report"] = {}
        self.metadata["verification_report"]["corruption_detected"] = is_corrupted

        return self.corrupted_files

    def load_config_file(self, target_path: str) -> None:
        """Helper to safely load config.json into metadata if available."""
        config_path = os.path.join(target_path, "config.json")
        if os.path.exists(config_path) and not check_file_corrupted(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self.metadata["raw_config"] = json.load(f)
            except Exception:
                self.metadata["raw_config"] = {}

    def scan_model_directory(self, path: Optional[str] = None) -> bool:
        start_time = time.perf_counter()

        if path is not None:
            self.model_path = path

        target_path = self.model_path

        if not target_path:
            self.is_validated = False
            self.from_cache = False
            self.performance_metrics["scan_time_ms"] = round((time.perf_counter() - start_time) * 1000, 3)
            return False

        # Check Cache
        if self.use_cache and target_path in _METADATA_CACHE:
            cached_data = _METADATA_CACHE[target_path]
            self.is_validated = cached_data.get("is_validated", False)
            self.corrupted_files = list(cached_data.get("corrupted_files", []))
            self.shards = list(cached_data.get("shards", []))
            self.is_sharded = cached_data.get("is_sharded", False)
            self.metadata = copy.deepcopy(cached_data.get("metadata", self.metadata))
            self.from_cache = True
            self.performance_metrics["scan_time_ms"] = 0.0
            return self.is_validated

        self.from_cache = False

        if not check_directory_exists(target_path):
            self.is_validated = False
            self.performance_metrics["scan_time_ms"] = round((time.perf_counter() - start_time) * 1000, 3)
            return False

        # Perform Scan
        self.load_config_file(target_path)
        corrupted = self.detect_corrupted_files(target_path)
        self.detect_model_shards(target_path)

        self.is_validated = len(corrupted) == 0
        self.performance_metrics["scan_time_ms"] = round((time.perf_counter() - start_time) * 1000, 3)

        # Cache Scan Results (Valid or Invalid)
        if self.use_cache:
            _METADATA_CACHE[target_path] = {
                "is_validated": self.is_validated,
                "corrupted_files": list(self.corrupted_files),
                "shards": list(self.shards),
                "is_sharded": self.is_sharded,
                "metadata": copy.deepcopy(self.metadata)
            }

        return self.is_validated

    def scan_directory(self, path: Optional[str] = None) -> bool:
        return self.scan_model_directory(path)

    def verify_config_keys(self, required_keys: Optional[List[str]] = None) -> bool:
        start_time = time.perf_counter()
        raw_cfg = self.metadata.get("raw_config") or {}
        if required_keys is None:
            required_keys = ["hidden_size", "num_hidden_layers", "vocab_size"]

        is_valid = bool(raw_cfg) and all(k in raw_cfg for k in required_keys)
        if "verification_report" not in self.metadata:
            self.metadata["verification_report"] = {}
        self.metadata["verification_report"]["config_verified"] = is_valid

        self.performance_metrics["verification_time_ms"] = round((time.perf_counter() - start_time) * 1000, 3)
        return is_valid

    def estimate_parameter_count(self) -> float:
        cfg = self.metadata.get("raw_config") or {}
        hidden_size = cfg.get("hidden_size", 4096)
        num_layers = cfg.get("num_hidden_layers", 32)
        vocab_size = cfg.get("vocab_size", 32000)
        intermediate_size = cfg.get("intermediate_size", 11008)

        attn_params = 4 * (hidden_size ** 2)
        mlp_params = 3 * hidden_size * intermediate_size
        embed_params = vocab_size * hidden_size

        raw_estimated = (num_layers * (attn_params + mlp_params)) + embed_params
        estimated_in_billions = round(raw_estimated / 1e9, 2)
        self.metadata["param_count"] = estimated_in_billions
        return estimated_in_billions

    def load_safely(self) -> Dict[str, str]:
        start_time = time.perf_counter()
        try:
            sandbox = SandboxEnvironment(self.model_path)

            if hasattr(sandbox, "initialize_sandbox"):
                sandbox.initialize_sandbox()

            if hasattr(sandbox, "execute_safely"):
                res = sandbox.execute_safely()
            else:
                res = sandbox.run("load")

            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)
            self.performance_metrics["load_time_ms"] = elapsed_ms

            if not res or res in ("Intercepted", "failed"):
                return {"status": "Intercepted"}

            return {"status": "SUCCESS"}
        except Exception as e:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)
            self.performance_metrics["load_time_ms"] = elapsed_ms
            return {
                "status": "Intercepted",
                "message": "Security runtime failure",
                "error_details": str(e)
            }

    def get_memory_projection(
        self, 
        param_count: Optional[float] = None, 
        precision: str = "float16"
    ) -> Dict[str, Any]:
        count = param_count if param_count is not None else (self.metadata.get("param_count") or self.estimate_parameter_count())
        return calculate_memory_projection(param_count=count, precision=precision)

    def get_performance_metrics(self) -> Dict[str, float]:
        self.performance_metrics["total_execution_time_ms"] = round(
            sum([
                self.performance_metrics.get("scan_time_ms", 0.0),
                self.performance_metrics.get("verification_time_ms", 0.0),
                self.performance_metrics.get("load_time_ms", 0.0)
            ]), 3
        )
        return self.performance_metrics

    def generate_validation_report(self) -> Dict[str, Any]:
        projection = self.get_memory_projection()
        metrics = self.get_performance_metrics()
        report_status = "PASS" if self.is_validated and not self.corrupted_files else "FAIL"

        return {
            "validation_status": report_status,
            "target_model_path": self.model_path,
            "is_validated": self.is_validated,
            "from_cache": self.from_cache,
            "is_sharded": self.is_sharded,
            "shard_count": len(self.shards),
            "corrupted_files_count": len(self.corrupted_files),
            "corrupted_files": self.corrupted_files,
            "verification_checks": self.metadata.get("verification_report", {}),
            "estimated_parameters_b": self.metadata.get("param_count", 0.0),
            "memory_requirements": projection,
            "performance_latency": metrics,
        }

    def export_validation_report(self, output_path: str = "validation_report.json") -> bool:
        try:
            report_data = self.generate_validation_report()
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=4)
            return True
        except Exception:
            return False

    def export_metadata(self) -> Dict[str, Any]:
        return self.generate_validation_report()

    def export_metadata_to_file(self, output_path: str = "model_metadata.json") -> bool:
        return self.export_validation_report(output_path)