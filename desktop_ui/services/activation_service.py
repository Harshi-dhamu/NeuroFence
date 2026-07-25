import torch

from activation_tracker import (
    ActivationTracker
)


class ActivationService:

    def __init__(self):
        self.tracker = None

    def analyze(self, model):

        self.tracker = ActivationTracker(model)

        try:

            dummy_input = torch.randn(
                1,
                10
            )

            activations = (
                self.tracker.track_activation(
                    dummy_input
                )
            )

            statistics = (
                self.tracker.get_statistics()
            )

            neuron_activity = (
                self.tracker.analyze_neuron_activity()
            )

            return {
                "activations": activations,
                "statistics": statistics,
                "neuron_activity": neuron_activity,
            }

        except Exception as exc:

            return {
                "activations": {},
                "statistics": {},
                "neuron_activity": {},
                "error": str(exc),
            }