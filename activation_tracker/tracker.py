"""
tracker.py

Main Activation Tracker interface.
"""

from typing import Any, Dict

from .hooks import HookManager


class ActivationTracker:
    """
    Tracks intermediate neural network activations.
    """

    def __init__(self, model: Any):
        self.model = model
        self.hook_manager = HookManager()

    def start_tracking(self):
        """
        Register forward hooks.
        """
        self.hook_manager.register_hooks(self.model)

    def stop_tracking(self):
        """
        Remove hooks.
        """
        self.hook_manager.remove_hooks()

    def get_activations(self) -> Dict[str, Any]:
        """
        Return captured activations.
        """
        return self.hook_manager.activations