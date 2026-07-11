"""
utils.py - Internal Utility Functions
Helper methods dedicated to local file system validation and cryptographic checks.
"""

import os

def check_directory_exists(path: str) -> bool:
    """
    Safely checks if a local directory exists.
    
    :param path: Target file system path.
    :return: True if directory exists, False otherwise.
    """
    return os.path.isdir(path)