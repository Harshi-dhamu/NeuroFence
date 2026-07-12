"""
Activation Tracker Package

This package provides utilities for tracking intermediate neural
network activations during inference.

Modules:
    tracker  : Main ActivationTracker interface
    hooks    : Forward hook management
    analyzer : Activation analysis utilities
    utils    : Shared helper functions
"""

from .tracker import ActivationTracker

__all__ = ["ActivationTracker"]