class ActivationService:

    def __init__(self):
        self.tracker = None

    def analyze(self, model):

        try:
            # Imported here, not at module load time, so opening the
            # NeuroFence UI never requires torch / activation_tracker
            # to be importable. Only an actual scan does.
            import torch
            from activation_tracker import ActivationTracker

            self.tracker = ActivationTracker(model)

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