"""
core.py - Core Model Loading and Verification Engine
Responsible for safe interaction, structural validation, memory analysis, 
comprehensive summary generation, and system logging of local Hugging Face models.
"""

import os
import logging
from typing import Dict, Any, Optional
from .utils import (
    check_directory_exists, locate_model_files, verify_file_integrity, 
    load_json_config, calculate_precision_footprint
)
from .sandbox import SandboxEnvironment, SandboxSecurityError

# --- DAY 10 LOGGING SETUP ---
logger = logging.getLogger("NeuroFence.ModelLoader")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if the module is re-imported
if not logger.handlers:
    log_file_path = os.path.abspath("loader.log")
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] (Loader): %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
# -----------------------------

class ModelLoader:
    """
    Handles the safe verification, metadata extraction, deep file auditing,
    memory profiling, logging, and unified summary generation of local Hugging Face models.
    """
    
    def __init__(self, model_path: str):
        """
        Initializes the ModelLoader with a target local directory.
        
        :param model_path: Path to the local model directory.
        """
        self.model_path = os.path.abspath(model_path)
        self.model_name: Optional[str] = os.path.basename(self.model_path)
        self.is_validated: bool = False
        self.metadata: Dict[str, Any] = {
            "detected_safetensors": [],
            "detected_pytorch_bin": [],
            "has_config": False,
            "raw_config": {},
            "raw_tokenizer_config": {},
            "verification_report": {
                "config_verified": False,
                "tokenizer_verified": False,
                "weights_verified": False
            }
        }
        logger.info(f"Initialized ModelLoader for target path: {self.model_path}")

    def scan_model_directory(self) -> bool:
        """Scans the local directory to discover weights and layout configurations."""
        logger.info(f"Scanning directory footprint for model: {self.model_name}")
        if not check_directory_exists(self.model_path):
            logger.error(f"Scan failed: Target directory does not exist -> {self.model_path}")
            self.is_validated = False
            return False

        config_path = os.path.join(self.model_path, "config.json")
        self.metadata["has_config"] = os.path.exists(config_path)

        self.metadata["detected_safetensors"] = locate_model_files(self.model_path, ".safetensors")
        self.metadata["detected_pytorch_bin"] = locate_model_files(self.model_path, ".bin")

        logger.info(f"Scan completed. Found Safetensors: {len(self.metadata['detected_safetensors'])}, PyTorch Binaries: {len(self.metadata['detected_pytorch_bin'])}")
        return True

    def verify_config_keys(self) -> bool:
        """Deep-audits config.json to ensure critical LLM hyperparameter definitions exist."""
        config = self.metadata.get("raw_config", {})
        if not config:
            logger.warning("Config verification aborted: No loaded configuration content found.")
            return False

        critical_keys = ["model_type", "vocab_size", "hidden_size", "num_hidden_layers"]
        has_keys = all(key in config for key in critical_keys)
        
        if not has_keys:
            missing = [k for k in critical_keys if k not in config]
            logger.warning(f"Config validation failed. Missing structural parameters: {missing}")
        else:
            logger.info("Config structural parameters verified successfully.")

        self.metadata["verification_report"]["config_verified"] = has_keys
        return has_keys

    def verify_tokenizer_files(self) -> bool:
        """Verifies that tokenizer infrastructure configuration exists and is valid."""
        tokenizer_config_path = os.path.join(self.model_path, "tokenizer_config.json")
        tokenizer_model_path = os.path.join(self.model_path, "tokenizer.json")
        legacy_vocab_path = os.path.join(self.model_path, "vocab.json")

        has_config = verify_file_integrity(tokenizer_config_path)
        has_vocab = verify_file_integrity(tokenizer_model_path) or verify_file_integrity(legacy_vocab_path)

        is_tokenizer_valid = has_config and has_vocab
        if not is_tokenizer_valid:
            logger.warning(f"Tokenizer check failed. Config available: {has_config}, Vocab/Matrix available: {has_vocab}")
        else:
            logger.info("Tokenizer layout validation successful.")

        self.metadata["verification_report"]["tokenizer_verified"] = is_tokenizer_valid
        return is_tokenizer_valid

    def verify_weight_layout(self) -> bool:
        """Performs validation against model weight splits to ensure files are valid."""
        safetensors_pool = self.metadata["detected_safetensors"]
        pytorch_pool = self.metadata["detected_pytorch_bin"]

        active_pool = safetensors_pool if safetensors_pool else pytorch_pool
        if not active_pool:
            logger.error("Weight layout validation failed: No tensor files found.")
            return False

        for weight_file in active_pool:
            full_weight_path = os.path.join(self.model_path, weight_file)
            if not verify_file_integrity(full_weight_path):
                logger.error(f"Weight file integrity compromised: {weight_file}")
                return False

        logger.info(f"Weight validation cleared for {len(active_pool)} binary components.")
        self.metadata["verification_report"]["weights_verified"] = True
        return True

    def validate_weights(self) -> bool:
        """Executes the full, strict multi-stage verification pipeline."""
        logger.info("Starting strict multi-stage structural validation pipeline.")
        if not self.scan_model_directory():
            self.is_validated = False
            return False

        config_path = os.path.join(self.model_path, "config.json")
        if not self.metadata["has_config"] or not verify_file_integrity(config_path):
            logger.error("Validation pipeline aborted: Core config.json missing or empty.")
            self.is_validated = False
            return False

        self.extract_metadata()

        config_ok = self.verify_config_keys()
        tokenizer_ok = self.verify_tokenizer_files()
        weights_ok = self.verify_weight_layout()

        self.is_validated = bool(config_ok and tokenizer_ok and weights_ok)
        if self.is_validated:
            logger.info(f"Model '{self.model_name}' cleared validation successfully.")
        else:
            logger.error(f"Model '{self.model_name}' failed security and structural verification checks.")
        return self.is_validated

    def detect_framework(self) -> str:
        """Detects the model weight distribution standard format."""
        if self.metadata["detected_safetensors"]:
            return "Safetensors"
        elif self.metadata["detected_pytorch_bin"]:
            return "PyTorch (Legacy)"
        return "Unknown"

    def detect_architecture(self) -> str:
        """Identifies the concrete model architecture type defined inside the config."""
        config = self.metadata.get("raw_config", {})
        if "architectures" in config and isinstance(config["architectures"], list) and config["architectures"]:
            return str(config["architectures"][0])
        elif "model_type" in config:
            return str(config["model_type"]).capitalize()
        return "Unknown Architecture"

    def get_total_disk_size_bytes(self) -> int:
        """Calculates the aggregate on-disk storage size of all detected weight files."""
        total_bytes = 0
        safetensors_pool = self.metadata["detected_safetensors"]
        pytorch_pool = self.metadata["detected_pytorch_bin"]
        active_pool = safetensors_pool if safetensors_pool else pytorch_pool

        for file_name in active_pool:
            file_path = os.path.join(self.model_path, file_name)
            if os.path.exists(file_path):
                total_bytes += os.path.getsize(file_path)
        return total_bytes

    def estimate_parameter_count(self) -> float:
        """Heuristically estimates the total model parameter count in billions."""
        config = self.metadata.get("raw_config", {})
        if not config:
            return 0.0

        if "num_parameters" in config:
            return round(float(config["num_parameters"]) / 1e9, 2)

        hidden_size = config.get("hidden_size", 0)
        num_layers = config.get("num_hidden_layers", 0)
        vocab_size = config.get("vocab_size", 0)
        intermediate_size = config.get("intermediate_size", hidden_size * 4)

        if not (hidden_size and num_layers):
            return 0.0

        embeddings = vocab_size * hidden_size
        attention_per_layer = 4 * (hidden_size ** 2)
        mlp_per_layer = 3 * hidden_size * intermediate_size
        layer_total = num_layers * (attention_per_layer + mlp_per_layer)
        
        calculated_total = embeddings + layer_total
        return round(calculated_total / 1e9, 2)

    def generate_memory_profile(self) -> Dict[str, Any]:
        """Builds a comprehensive memory matrix profiling estimation metrics."""
        param_count_b = self.estimate_parameter_count()
        disk_size_bytes = self.get_total_disk_size_bytes()
        
        return {
            "estimated_parameters_billions": param_count_b,
            "disk_size_gb": round(disk_size_bytes / (1024 ** 3), 2),
            "estimated_runtime_ram_requirement": {
                "fp32_precision_gb": calculate_precision_footprint(param_count_b, 32),
                "fp16_precision_gb": calculate_precision_footprint(param_count_b, 16),
                "int8_quantized_gb": calculate_precision_footprint(param_count_b, 8),
                "int4_quantized_gb": calculate_precision_footprint(param_count_b, 4)
            }
        }

    def generate_model_summary(self) -> Dict[str, Any]:
        """Gathers structural metadata, validation vectors, and hardware footprints."""
        self.extract_metadata()
        config = self.metadata.get("raw_config", {})
        tokenizer = self.metadata.get("raw_tokenizer_config", {})
        mem_profile = self.generate_memory_profile()

        return {
            "model_identity": {
                "name": self.model_name,
                "local_path": self.model_path
            },
            "architecture_details": {
                "architecture": self.detect_architecture(),
                "layers_count": config.get("num_hidden_layers", "Unknown"),
                "attention_heads": config.get("num_attention_heads", "Unknown"),
                "hidden_size": config.get("hidden_size", "Unknown")
            },
            "tensor_properties": {
                "framework": self.detect_framework(),
                "parameter_count_b": mem_profile["estimated_parameters_billions"],
                "disk_storage_gb": mem_profile["disk_size_gb"]
            },
            "tokenizer_properties": {
                "has_tokenizer_config": bool(tokenizer),
                "tokenizer_class": tokenizer.get("tokenizer_class", "Unknown Tokenizer"),
                "vocabulary_size": config.get("vocab_size", "Unknown")
            },
            "security_status": {
                "is_structurally_validated": self.is_validated,
                "checks_passed": self.metadata["verification_report"]
            },
            "hardware_projections": mem_profile["estimated_runtime_ram_requirement"]
        }

    def extract_metadata(self) -> Dict[str, Any]:
        """Parses config.json and tokenizer_config.json to extract deep metadata parameters."""
        config_path = os.path.join(self.model_path, "config.json")
        config_data = load_json_config(config_path)
        if config_data:
            self.metadata["raw_config"] = config_data

        tokenizer_path = os.path.join(self.model_path, "tokenizer_config.json")
        tokenizer_data = load_json_config(tokenizer_path)
        if tokenizer_data:
            self.metadata["raw_tokenizer_config"] = tokenizer_data

        return self.metadata

    def get_model_info(self) -> Dict[str, Any]:
        """Backward compatible metadata summary fetcher pointing to the summary generator."""
        return self.generate_model_summary()

    def _internal_weight_loader_payload(self) -> str:
        """Internal target payload simulation representing backend weight mounting."""
        if not self.is_validated:
            raise ValueError("Execution blocked: Deep verification pipeline has not cleared.")
        return "Success: Isolated payload model state loaded into sandbox memory space."

    def load_safely(self) -> Dict[str, Any]:
        """Initializes the Model Sandbox environment and safely passes execution."""
        logger.info(f"Attempting secure runtime staging execution for model: {self.model_name}")
        response_summary = {"status": "Failed", "message": "", "error_details": None}
        
        if not self.is_validated and not self.validate_weights():
            response_summary["message"] = "Model failed strict structural verification checks."
            logger.error("Execution terminated: Model verification sequence failed.")
            return response_summary

        sandbox = SandboxEnvironment()
        logger.info("Initializing security sandbox context layer.")
        if not sandbox.initialize_sandbox():
            response_summary["message"] = "Could not securely provision Sandbox Environment."
            logger.critical("Critical error: Sandbox execution space configuration failed.")
            return response_summary

        try:
            logger.info("Routing logic execution tracking directly into isolated sandbox.")
            result_message = sandbox.execute_safely(self._internal_weight_loader_payload)
            response_summary["status"] = "Isolated"
            response_summary["message"] = result_message
            logger.info("Staged model payload successfully mounted into sandbox memory.")
        except SandboxSecurityError as sse:
            response_summary["status"] = "Intercepted"
            response_summary["message"] = "Security runtime failure occurred during isolated setup."
            response_summary["error_details"] = str(sse)
            logger.critical(f"Security runtime interception triggered! Details: {str(sse)}")
        finally:
            logger.info("Tearing down active sandbox instances.")
            sandbox.close_sandbox()

        return response_summary