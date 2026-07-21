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
    
    @staticmethod
    def compute_layer_scores(
        activations,
        threshold: float = 1e-5,
    ):
        """Compute activity-related scores for each tracked layer."""

        layer_scores = {}

        for layer_name, info in activations.items():

            tensor = info["activation"]

            total = tensor.numel()

            active = int((torch.abs(tensor) > threshold).sum().item())

            dormant = total - active

            activity_score = active / total

            dormant_score = dormant / total

            activation_spread = float(
                torch.max(tensor) - torch.min(tensor)
            )

            layer_scores[layer_name] = {
                "layer_type": info["layer_type"],
                "activity_score": activity_score,
                "dormant_score": dormant_score,
                "activation_spread": activation_spread,
                "active_neurons": active,
                "dormant_neurons": dormant,
            }

        return layer_scores
    
    @staticmethod
    def compare_activations(
        activations_a,
        activations_b,
    ):
        """Compare two activation dictionaries layer by layer.
    """

        comparison = {}

        common_layers = (
            activations_a.keys() &
            activations_b.keys()
        )

        for layer in common_layers:

            tensor_a = activations_a[layer]["activation"]
            tensor_b = activations_b[layer]["activation"]

            if tensor_a.shape != tensor_b.shape:

                comparison[layer] = {
                    "layer_type": activations_a[layer]["layer_type"],
                    "status": "shape_mismatch",
                    "shape_a": tuple(tensor_a.shape),
                    "shape_b": tuple(tensor_b.shape),
                }

                continue

            diff = tensor_a - tensor_b

            comparison[layer] = {
                "layer_type": activations_a[layer]["layer_type"],
                "status": "ok",
                "shape": tuple(diff.shape),
                "mean_difference": float(diff.mean()),
                "mean_absolute_difference": float(diff.abs().mean()),
                "maximum_difference": float(diff.abs().max()),
                "difference_matrix": diff.numpy().tolist(),
            }
        return comparison
    
    @staticmethod
    def generate_comparison_report(comparison_results):
        """
        Generate a summary report from activation comparison results.
        """

        report = {
            "total_layers": 0,
            "average_difference": 0.0,
            "most_changed_layer": None,
            "highest_difference": 0.0,
            "layers": {}
        }

        total_difference = 0.0

        for layer_name, info in comparison_results.items():

            if info["status"] != "ok":
                continue

            difference = info["mean_absolute_difference"]

            report["layers"][layer_name] = {
                "layer_type": info.get("layer_type", "Unknown"),
                "mean_absolute_difference": difference,
                "maximum_difference": info["maximum_difference"]
            }

            total_difference += difference
            report["total_layers"] += 1

            if difference > report["highest_difference"]:
                report["highest_difference"] = difference

                report["most_changed_layer"] = {
                    "layer_name": layer_name,
                    "layer_type": info["layer_type"],
                    "mean_absolute_difference": difference,
                    "maximum_difference": info["maximum_difference"],
                }
        if report["total_layers"] > 0:
            report["average_difference"] = (
                total_difference / report["total_layers"]
            )

        return report