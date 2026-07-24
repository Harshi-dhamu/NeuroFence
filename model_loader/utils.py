"""
utils.py - Internal Utility Functions
Helper methods dedicated to local file system validation, cryptographic checks, and memory profiling math.
"""

import os
import json
from typing import List, Dict, Any, Optional

def check_directory_exists(path: str) -> bool:
    """
    Safely checks if a local directory exists.
    
    :param path: Target file system path.
    :return: True if directory exists, False otherwise.
    """
    return os.path.isdir(path)

def locate_model_files(directory_path: str, extension: str) -> List[str]:
    """
    Scans the directory for files matching a specific extension.
    
    :param directory_path: The folder to scan.
    :param extension: File extension to look for (e.g., '.safetensors', '.bin').
    :return: A list of matching filenames.
    """
    if not check_directory_exists(directory_path):
        return []
    
    try:
        return [f for f in os.listdir(directory_path) if f.endswith(extension)]
    except OSError:
        return []

def verify_file_integrity(file_path: str) -> bool:
    """
    Validates if a file exists and is structurally non-empty.
    Ensures corrupted/0-byte downloads are flagged immediately.
    
    :param file_path: Absolute path to the file.
    :return: True if the file is valid, False otherwise.
    """
    if not os.path.exists(file_path):
        return False
        
    try:
        return os.path.getsize(file_path) > 0
    except OSError:
        return False

def load_json_config(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Safely reads and deserializes a JSON file.
    Catches errors gracefully to prevent system-wide loader crashes.
    
    :param file_path: Path to the target JSON configuration.
    :return: Dictionary with configuration options, or None if parsing fails.
    """
    if not verify_file_integrity(file_path):
        return None
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, ValueError):
        return None

def calculate_precision_footprint(param_count_billions: float, precision_bits: int) -> float:
    """
    Calculates the expected memory footprint in Gigabytes for a given parameter count and precision.
    Includes a realistic 20% system overhead buffer factor.
    
    :param param_count_billions: Count of parameters expressed in Billions (e.g., 7.0 for 7B).
    :param precision_bits: Quantization bit depth (32, 16, 8, 4).
    :return: Estimated memory requirement in Gigabytes.
    """
    if param_count_billions <= 0:
        return 0.0
    
    # Bytes per parameter mapping
    bytes_per_param = precision_bits / 8.0
    
    # Pure weight size in GB: (Params * 10^9 * Bytes) / 10^9 => Params * Bytes
    base_weight_gb = param_count_billions * bytes_per_param
    
    # Add a standard 20% runtime overhead for context windows, activations, and KV cache bounds
    overhead_factor = 1.20
    return round(base_weight_gb * overhead_factor, 2)