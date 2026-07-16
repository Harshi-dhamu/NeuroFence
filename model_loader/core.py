"""
core.py - Core Model Loading and Verification Engine
Responsible for safe interaction and deep structural validation of local Hugging Face model directories.
"""

import os
from typing import Dict, Any, Optional
from .utils import check_directory_exists, locate_model_files, verify_file_integrity, load_json_config
from .sandbox import SandboxEnvironment, SandboxSecurityError

class ModelLoader:
    """
    Handles the safe verification, metadata extraction, deep file auditing,
    and isolated loading of local Hugging Face transformer models.
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

    def scan_model_directory(self) -> bool:
        """
        Scans the local directory to discover weights and layout configurations.
        Updates internal metadata map based on discovered components.
        """
        if not check_directory_exists(self.model_path):
            self.is_validated = False
            return False

        config_path = os.path.join(self.model_path, "config.json")
        self.metadata["has_config"] = os.path.exists(config_path)

        self.metadata["detected_safetensors"] = locate_model_files(self.model_path, ".safetensors")
        self.metadata["detected_pytorch_bin"] = locate_model_files(self.model_path, ".bin")

        return True

    def verify_config_keys(self) -> bool:
        """
        Deep-audits config.json to ensure critical LLM hyperparameter definitions exist.
        
        :return: True if the structural configuration satisfies model criteria, False otherwise.
        """
        config = self.metadata.get("raw_config", {})
        if not config:
            return False

        # Essential architectural keys required by model runners
        critical_keys = ["model_type", "vocab_size", "hidden_size", "num_hidden_layers"]
        has_keys = all(key in config for key in critical_keys)
        
        self.metadata["verification_report"]["config_verified"] = has_keys
        return has_keys

    def verify_tokenizer_files(self) -> bool:
        """
        Verifies that tokenizer infrastructure configuration exists and is valid.
        Checks for matching config and vocabulary definitions.
        
        :return: True if tokenizer ecosystem passes structural presence checks.
        """
        # A tokenizer directory should ideally contain a config and an operational map layer
        tokenizer_config_path = os.path.join(self.model_path, "tokenizer_config.json")
        tokenizer_model_path = os.path.join(self.model_path, "tokenizer.json")
        legacy_vocab_path = os.path.join(self.model_path, "vocab.json")

        has_config = verify_file_integrity(tokenizer_config_path)
        has_vocab = verify_file_integrity(tokenizer_model_path) or verify_file_integrity(legacy_vocab_path)

        is_tokenizer_valid = has_config and has_vocab
        self.metadata["verification_report"]["tokenizer_verified"] = is_tokenizer_valid
        return is_tokenizer_valid

    def verify_weight_layout(self) -> bool:
        """
        Performs validation against model weight splits to ensure files are valid.
        
        :return: True if weight binaries pass integrity parameters.
        """
        safetensors_pool = self.metadata["detected_safetensors"]
        pytorch_pool = self.metadata["detected_pytorch_bin"]

        active_pool = safetensors_pool if safetensors_pool else pytorch_pool
        if not active_pool:
            return False

        for weight_file in active_pool:
            full_weight_path = os.path.join(self.model_path, weight_file)
            if not verify_file_integrity(full_weight_path):
                return False

        self.metadata["verification_report"]["weights_verified"] = True
        return True

    def validate_weights(self) -> bool:
        """
        Executes the full, strict multi-stage verification pipeline.
        
        :return: True if all model layers pass verification tests, False otherwise.
        """
        # 1. Base Scan
        if not self.scan_model_directory():
            self.is_validated = False
            return False

        # 2. Basic file integrity check for config.json
        config_path = os.path.join(self.model_path, "config.json")
        if not self.metadata["has_config"] or not verify_file_integrity(config_path):
            self.is_validated = False
            return False

        # Load metadata configurations for deep key auditing
        self.extract_metadata()

        # 3. Comprehensive verification run
        config_ok = self.verify_config_keys()
        tokenizer_ok = self.verify_tokenizer_files()
        weights_ok = self.verify_weight_layout()

        # Enforce all three critical pillars pass inspection
        self.is_validated = bool(config_ok and tokenizer_ok and weights_ok)
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
        """Compiles a summary dictionary describing structural properties and verification statuses."""
        self.extract_metadata()
        config = self.metadata.get("raw_config", {})
        tokenizer = self.metadata.get("raw_tokenizer_config", {})

        info_summary = {
            "model_name": self.model_name,
            "architecture": self.detect_architecture(),
            "framework": self.detect_framework(),
            "has_tokenizer": bool(tokenizer),
            "tokenizer_class": tokenizer.get("tokenizer_class", "Unknown Tokenizer"),
            "vocab_size": config.get("vocab_size", "Unknown"),
            "hidden_size": config.get("hidden_size", "Unknown"),
            "num_hidden_layers": config.get("num_hidden_layers", "Unknown"),
            "num_attention_heads": config.get("num_attention_heads", "Unknown"),
            "verification_status": self.metadata["verification_report"]
        }
        return info_summary

    def _internal_weight_loader_payload(self) -> str:
        """Internal target payload simulation representing backend weight mounting."""
        if not self.is_validated:
            raise ValueError("Execution blocked: Deep verification pipeline has not cleared.")
        return "Success: Isolated payload model state loaded into sandbox memory space."

    def load_safely(self) -> Dict[str, Any]:
        """Initializes the Model Sandbox environment and safely passes execution to the verified payload."""
        response_summary = {"status": "Failed", "message": "", "error_details": None}
        
        if not self.is_validated and not self.validate_weights():
            response_summary["message"] = "Model failed strict structural verification checks."
            return response_summary

        sandbox = SandboxEnvironment()
        if not sandbox.initialize_sandbox():
            response_summary["message"] = "Could not securely provision Sandbox Environment."
            return response_summary

        try:
            result_message = sandbox.execute_safely(self._internal_weight_loader_payload)
            response_summary["status"] = "Isolated"
            response_summary["message"] = result_message
        except SandboxSecurityError as sse:
            response_summary["status"] = "Intercepted"
            response_summary["message"] = "Security runtime failure occurred during isolated setup."
            response_summary["error_details"] = str(sse)
        finally:
            sandbox.close_sandbox()

        return response_summary