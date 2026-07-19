"""
tracker.py

Main Activation Tracker interface.
"""

from typing import Any, Dict

from .hooks import HookManager
from .analyzer import ActivationAnalyzer
from .logger import ActivationLogger

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

    def get_statistics(self):
        """
        Return activation statistics.
        """
        return ActivationAnalyzer.compute_statistics(
            self.get_activations()
        )
    def analyze_neuron_activity(self, threshold=1e-5):
        """Analyze neuron activity for all tracked layers."""

        return ActivationAnalyzer.analyze_neuron_activity(
        self.get_activations(),
        threshold,
    )

    def export_statistics(self, output_file):
        """ Export activation statistics to JSON."""

        statistics = self.get_statistics()

        ActivationLogger.export_statistics(
            statistics,
            output_file,
        )


    def export_numpy(self, output_directory):
        """Export activation tensors as NumPy files."""

        ActivationLogger.export_numpy(
            self.get_activations(),
            output_directory,
        )
    def get_layer_summary(self):
        """
        Return layer summary information.
        """

        return ActivationAnalyzer.prepare_layer_summary(
            self.get_activations()
        )
    
    def get_neuron_data(self):
        """
        Return neuron activation values.
        """

        return ActivationAnalyzer.prepare_neuron_data(
            self.get_activations()
        )
    
    def get_heatmap_data(self):
        """
        Return heatmap-ready activation data.
        """

        return ActivationAnalyzer.prepare_heatmap_data(
            self.get_activations()
        )
    
    def get_layer_scores(self, threshold=1e-5):
        """Return activity scores for every tracked layer."""

        return ActivationAnalyzer.compute_layer_scores(
            self.get_activations(),
            threshold,
    )

    def compare_with(
        self,
        other_activations,
    ):
        """
        Compare current activations with another activation set.
        """

        return ActivationAnalyzer.compare_activations(
            self.get_activations(),
            other_activations,
        )