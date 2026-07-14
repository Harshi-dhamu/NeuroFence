"""
analyzer.py

Activation statistics for tracked neural network layers.
"""

from typing import Dict, Any

import torch


class ActivationAnalyzer:
    """
    Computes statistics for stored activations.
    """

    @staticmethod
    def compute_statistics(
        activations: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Compute statistics for every tracked layer.
        """

        statistics = {}

        for layer_name, info in activations.items():

            tensor = info["activation"]

            statistics[layer_name] = {
                "layer_type": info["layer_type"],
                "shape": info["shape"],
                "mean": float(torch.mean(tensor)),
                "variance": float(torch.var(tensor)),
                "maximum": float(torch.max(tensor)),
                "minimum": float(torch.min(tensor)),
            }

        return statistics