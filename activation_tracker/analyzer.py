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
    def prepare_normalized_heatmap_data(activations):
        """
        Prepare normalized activation matrices for heatmap visualization.
        Values are scaled between 0 and 1.
        """

        heatmaps = {}

        for layer_name, info in activations.items():

            tensor = info["activation"].float()

            minimum = tensor.min()
            maximum = tensor.max()

            if maximum == minimum:
                normalized = torch.zeros_like(tensor)
            else:
                normalized = (
                    (tensor - minimum)
                    / (maximum - minimum)
                )

            heatmaps[layer_name] = normalized.tolist()

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
         activations_a: Dict[str, Dict[str, Any]],
         activations_b: Dict[str, Dict[str, Any]],
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

    @staticmethod
    def rank_layers_by_activity(
        activations,
        threshold: float = 1e-5,
    ):
        """
        Rank tracked layers based on neuron activity.
        """

        scores = ActivationAnalyzer.compute_layer_scores(
            activations,
            threshold,
        )

        ranking = []

        for layer_name, info in scores.items():

            ranking.append(
                {
                    "layer_name": layer_name,
                    "layer_type": info["layer_type"],
                    "activity_score": info["activity_score"],
                    "active_neurons": info["active_neurons"],
                    "dormant_neurons": info["dormant_neurons"],
                }
            )

        ranking.sort(
            key=lambda layer: layer["activity_score"],
            reverse=True,
        )

        return ranking


    @staticmethod
    def analyze_dead_neurons(
        activations,
        threshold: float = 1e-5,
    ):
        """
        Analyze dead neuron severity for each tracked layer.
        """

        activity = ActivationAnalyzer.analyze_neuron_activity(
            activations,
            threshold,
        )

        results = {}

        for layer_name, info in activity.items():

            dormant_ratio = info["dormant_ratio"]

            if dormant_ratio < 0.25:
                severity = "Low"

            elif dormant_ratio < 0.50:
                severity = "Moderate"

            elif dormant_ratio < 0.75:
                severity = "High"

            else:
                severity = "Critical"

            results[layer_name] = {
                "layer_type": info["layer_type"],
                "total_neurons": info["total_neurons"],
                "active_neurons": info["active_neurons"],
                "dormant_neurons": info["dormant_neurons"],
                "activation_frequency": info["activation_frequency"],
                "dormant_ratio": dormant_ratio,
                "threshold": threshold,
                "severity": severity,
            }

        return results
    @staticmethod
    def classify_anomaly_severity(
        activations,
        threshold: float = 1e-5,
    ):
        """
        Classify anomaly severity for each tracked layer.
        """

        activity = ActivationAnalyzer.analyze_neuron_activity(
            activations,
            threshold,
        )

        results = {}

        for layer_name, info in activity.items():

            ratio = info["dormant_ratio"]

            if ratio < 0.20:
                severity = "Normal"
            elif ratio < 0.40:
                severity = "Low"
            elif ratio < 0.60:
                severity = "Medium"
            elif ratio < 0.80:
                severity = "High"
            else:
                severity = "Critical"

            results[layer_name] = {
                **info,
                "severity": severity,
            }

        return results

    @staticmethod
    def analyze_activation_trends(
        activation_history,
        threshold: float = 1e-5,
    ):
        """
        Analyze activation trends across multiple inference runs.
        """

        if not activation_history:
            return {}

        layer_names = activation_history[0].keys()

        trends = {}

        for layer_name in layer_names:

            activity_scores = []

            for snapshot in activation_history:

                if layer_name not in snapshot:
                    continue

                tensor = snapshot[layer_name]["activation"]

                total = tensor.numel()

                if total == 0:
                    activity_score = 0.0
                else:
                    active = int(
                        (torch.abs(tensor) > threshold).sum().item()
                    )

                    activity_score = active / total

                activity_scores.append(activity_score)

            if not activity_scores:
                continue

            first_score = activity_scores[0]
            last_score = activity_scores[-1]

            change = last_score - first_score

            if change > 0.05:
                trend = "increasing"
            elif change < -0.05:
                trend = "decreasing"
            else:
                trend = "stable"

            trends[layer_name] = {
                "activity_scores": activity_scores,
                "initial_activity": first_score,
                "final_activity": last_score,
                "change": change,
                "trend": trend,
            }

        return trends