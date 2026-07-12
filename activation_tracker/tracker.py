"""
tracker.py

Defines the public ActivationTracker interface.

Future versions will:
- Register forward hooks
- Capture activations
- Remove hooks safely
- Return collected activations
"""

from typing import Any, Dict


class ActivationTracker:
    """
    High-level interface for activation tracking.

    Parameters
    ----------
    model:
        Loaded neural network model.
    """

    def __init__(self, model: Any):
        self.model = model
        self.activations: Dict[str, Any] = {}

    def start_tracking(self):
        """
        Start activation tracking.

        Actual hook registration will be implemented later.
        """
        print("Activation tracking initialized.")

    def stop_tracking(self):
        """
        Stop activation tracking.

        Hook removal will be added later.
        """
        print("Activation tracking stopped.")

    def get_activations(self) -> Dict[str, Any]:
        """
        Return collected activations.

        Returns
        -------
        Dict[str, Any]
        """
        return self.activations