"""
core.py - Core Model Loading and Verification Engine
Responsible for safe interaction with local Hugging Face model directories.
"""

import os
from typing import Dict, Any, Optional
from .utils import check_directory_exists, locate_model_files, verify_file_integrity, load_json_config

class ModelLoader:
    """
    Handles the safe verification, metadata extraction, and loading
    of local Hugging Face transformer models.
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
            "raw_tokenizer_config": {}
        }

    def scan_model_directory(self) -> bool:
        """
        Scans the local directory to discover weights and layout configurations.
        Updates internal metadata map based on discovered components.
        
        :return: True if the base directory exists and contains files, False otherwise.
        """
        if not check_directory_exists(self.model_path):
            self.is_validated = False
            return False

        config_path = os.path.join(self.model_path, "config.json")
        self.metadata["has_config"] = os.path.exists(config_path)

        self.metadata["detected_safetensors"] = locate_model_files(self.model_path, ".safetensors")
        self.metadata["detected_pytorch_bin"] = locate_model_files(self.model_path, ".bin")

        return True

    def validate_weights(self) -> bool:
        """
        Verifies model weights consistency and integrity against safetensors/bin manifests.
        Ensures essential structural building blocks exist and are intact.
        
        :return: True if the model components pass structural verification tests, False otherwise.
        """
        self.scan_model_directory()

        config_path = os.path.join(self.model_path, "config.json")
        if not self.metadata["has_config"] or not verify_file_integrity(config_path):
            self.is_validated = False
            return False

        safetensors_pool = self.metadata["detected_safetensors"]
        pytorch_pool = self.metadata["detected_pytorch_bin"]

        if not safetensors_pool and not pytorch_pool:
            self.is_validated = False
            return False

        active_pool = safetensors_pool if safetensors_pool else pytorch_pool
        for weight_file in active_pool:
            full_weight_path = os.path.join(self.model_path, weight_file)
            if not verify_file_integrity(full_weight_path):
                self.is_validated = False
                return False

        self.is_validated = True
        return True

    def detect_framework(self) -> str:
        """
        Detects the model weight distribution standard format.
        
        :return: 'Safetensors', 'PyTorch (Legacy)', or 'Unknown'.
        """
        if self.metadata["detected_safetensors"]:
            return "Safetensors"
        elif self.metadata["detected_pytorch_bin"]:
            return "PyTorch (Legacy)"
        return "Unknown"

    def detect_architecture(self) -> str:
        """
        Identifies the concrete model architecture type defined inside the config.
        
        :return: String representing the model architecture category (e.g., 'Llama', 'Mistral').
        """
        config = self.metadata.get("raw_config", {})
        
        # Check standard Hugging Face properties
        if "architectures" in config and isinstance(config["architectures"], list) and config["architectures"]:
            return str(config["architectures"][0])
        elif "model_type" in config:
            return str(config["model_type"]).capitalize()
            
        return "Unknown Architecture"

    def extract_metadata(self) -> Dict[str, Any] :
        """
        Parses config.json and tokenizer_config.json to extract deep metadata parameters.
        
        :return: Updated metadata tracking dictionary.
        """
        if not self.is_validated and not self.validate_weights():
            return self.metadata

        # Load primary config
        config_path = os.path.join(self.model_path, "config.json")
        config_data = load_json_config(config_path)
        if config_data:
            self.metadata["raw_config"] = config_data

        # Load optional tokenizer configuration
        tokenizer_path = os.path.join(self.model_path, "tokenizer_config.json")
        tokenizer_data = load_json_config(tokenizer_path)
        if tokenizer_data:
            self.metadata["raw_tokenizer_config"] = tokenizer_data

        return self.metadata

    def get_model_info(self) -> Dict[str, Any]:
        """
        Compiles and builds a clean summary dictionary containing framework, 
        tokenizer visibility metrics, parameters, and architectural properties.
        
        :return: A high-level metadata overview mapping dashboard details.
        """
        self.extract_metadata()
        config = self.metadata.get("raw_config", {})
        tokenizer = self.metadata.get("raw_tokenizer_config", {})

        return {
            "model_name": self.model_name,
            "architecture": self.detect_architecture(),
            "framework": self.detect_framework(),
            "has_tokenizer": bool(tokenizer),
            "tokenizer_class": tokenizer.get("tokenizer_class", "Unknown Tokenizer"),
            "vocab_size": config.get("vocab_size", "Unknown"),
            "hidden_size": config.get("hidden_size", "Unknown"),
            "num_hidden_layers": config.get("num_hidden_layers", "Unknown"),
            "num_attention_heads": config.get("num_attention_heads", "Unknown")
        }

    def load_safely(self) -> Optional[Any]:
        """
        Loads the model tensors safely into memory inside the sandbox.
        (To be fully implemented in Day 6).
        """
        if not self.is_validated:
            return None
        return None