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
            "raw_config": {}
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

    def extract_metadata(self) -> Dict[str, Any]:
        """
        Parses config.json to extract basic model architecture details.
        
        :return: Updated metadata tracking dictionary.
        """
        if not self.is_validated and not self.validate_weights():
            return self.metadata

        config_path = os.path.join(self.model_path, "config.json")
        config_data = load_json_config(config_path)
        
        if config_data:
            self.metadata["raw_config"] = config_data
            
        return self.metadata

    def load_safely(self) -> Optional[Any]:
        """
        Loads the model tensors safely into memory inside the sandbox.
        (To be fully implemented in Day 6).
        """
        if not self.is_validated:
            return None
        return None