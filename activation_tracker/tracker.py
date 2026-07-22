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
        self._tracking = False

    def start_tracking(self):
        """
        Register forward hooks and start tracking.
        """

        self.hook_manager.clear_activations()
        self.hook_manager.register_hooks(self.model)

        self._tracking = True
    def get_activation_count(self):
        """
        Return the number of tracked layers.
        """

        return len(self.get_activations())

    def stop_tracking(self):
        """
        Remove forward hooks and stop tracking.
        """

        self.hook_manager.remove_hooks()

        self._tracking = False

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
    
    def generate_comparison_report(self, other_activations):
        """
        Compare activations and generate a summary report.
        """

        comparison = ActivationAnalyzer.compare_activations(
            self.get_activations(),
            other_activations,
        )

        return ActivationAnalyzer.generate_comparison_report(
            comparison
        )
    
    def is_tracking(self):
        """
        Return whether activation tracking is currently enabled.
        """

        return self._tracking
    
    def reset_tracker(self):
        """
        Reset all stored activations.
        """

        self.hook_manager.clear_activations()

    def track_activation(self, input_tensor):
        """
        Perform a single forward pass while tracking activations.
        """

        self.start_tracking()

        self.model(input_tensor)

        self.stop_tracking()

        return self.get_activations()
    
    def export_all(self, folder="activations"):
        """
        Export activations in all supported formats.
        """

        self.export_json(folder)

        self.export_numpy(folder)