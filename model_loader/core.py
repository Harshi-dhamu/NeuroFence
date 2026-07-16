"""
core.py - Core Model Loading and Verification Engine
Responsible for safe interaction with local Hugging Face model directories.
"""

import os
from typing import Dict, Any, Optional
from .utils import check_directory_exists, locate_model_files

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
            "has_config": False
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

        # Detect configuration file presence
        config_path = os.path.join(self.model_path, "config.json")
        self.metadata["has_config"] = os.path.exists(config_path)

        # Detect framework weights
        self.metadata["detected_safetensors"] = locate_model_files(self.model_path, ".safetensors")
        self.metadata["detected_pytorch_bin"] = locate_model_files(self.model_path, ".bin")

        # Basic path validation flag update
        self.is_validated = True
        return True

    def validate_weights(self) -> bool:
        """
        Verifies model weights consistency and integrity against safetensors/bin manifests.
        (To be fully implemented in Day 3).
        """
        return False

    def extract_metadata(self) -> Dict[str, Any]:
        """
        Parses config.json to extract model architecture specifics.
        (To be fully implemented in Day 4/5).
        """
        return self.metadata

    def load_safely(self) -> Optional[Any]:
        """
        Loads the model tensors safely into memory inside the sandbox.
        (To be fully implemented in Day 6).
        """
        if not self.is_validated:
            return None
        return None