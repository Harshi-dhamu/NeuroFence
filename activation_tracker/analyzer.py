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
    

    @staticmethod
    def prepare_layer_summary(activations):
        """Prepare summary information for each tracked layer."""

        summary = {}

        for layer_name, info in activations.items():

            tensor = info["activation"]

            summary[layer_name] = {
                "layer_type": info["layer_type"],
                "shape": list(tensor.shape),
                "num_neurons": tensor.numel(),
            }

        return summary
    @staticmethod
    def prepare_neuron_data(activations):
        """Convert activations into Python lists for visualization."""

        neuron_data = {}

        for layer_name, info in activations.items():

            neuron_data[layer_name] = (
                info["activation"]
                .flatten()
                .tolist()
            )

        return neuron_data
    

    @staticmethod
    def prepare_heatmap_data(activations):
        """Prepare activation matrices for heatmap visualization."""

        heatmaps = {}

        for layer_name, info in activations.items():

            heatmaps[layer_name] = (
                info["activation"]
                .numpy()
                .tolist()
            )

        return heatmaps