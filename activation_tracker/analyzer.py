"""
analyzer.py

Activation statistics and neuron activity analysis.
"""

from typing import Dict, Any

import torch


class ActivationAnalyzer:
    """
    Computes statistics and neuron activity metrics.
    """

    @staticmethod
    def compute_statistics(
        activations: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:

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

    @staticmethod
    def analyze_neuron_activity(
        activations: Dict[str, Dict[str, Any]],
        threshold: float = 1e-5,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Analyze neuron activity using a configurable threshold.
        """

        results = {}

        for layer_name, info in activations.items():

            tensor = info["activation"]

            active_mask = torch.abs(tensor) > threshold

            total = tensor.numel()
            active = int(active_mask.sum().item())
            dormant = total - active

            results[layer_name] = {
                "layer_type": info["layer_type"],
                "total_neurons": total,
                "active_neurons": active,
                "dormant_neurons": dormant,
                "activation_frequency": active / total,
                "dormant_ratio": dormant / total,
                "threshold": threshold,
            }

        return results