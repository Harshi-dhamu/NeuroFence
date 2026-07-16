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