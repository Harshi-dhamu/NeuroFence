"""
utils.py - Internal Utility Functions
Helper methods dedicated to local file system validation and cryptographic checks.
"""

import os
from typing import List

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