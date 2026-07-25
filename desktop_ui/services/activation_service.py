import torch
from activation_tracker import ActivationTracker


class ActivationService:

    def __init__(self):
        self.tracker = None

    def analyze(self, model, input_tensor=None):

        self.tracker = ActivationTracker(model)

        if input_tensor is None:
            input_tensor = torch.randn(1, 10)

        activations = self.tracker.track_activation(
            input_tensor
        )

        statistics = self.tracker.get_statistics()

        try:
            neuron_activity = (
                self.tracker.analyze_neuron_activity()
            )
        except Exception:
            neuron_activity = {}

        return {
            "activations": activations,
            "statistics": statistics,
            "neuron_activity": neuron_activity,
        }