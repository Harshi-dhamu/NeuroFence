"""Adapter for Akhina's Activation Tracker module."""
from __future__ import annotations


class ActivationServiceError(RuntimeError):
    """Raised when activation tracking cannot complete."""


class ActivationService:
    """Return placeholder activation and neuron statistics."""

    def run_activation_tracker(self, model_info: dict[str, object]) -> dict[str, object]:
        if not model_info.get("model_name"):
            raise ActivationServiceError("Activation tracking did not receive a loaded model.")

        # TODO(Akhina): replace with the real activation tracker and keep the
        # normalized keys below for controller/UI compatibility.
        return {
            "neurons_analyzed": 12_480,
            "dormant_neurons": 7,
            "anomalous_activations": 0,
            "activation_summary": "Activation patterns are within the expected baseline range.",
            "neuron_information": {
                "peak_activation": 0.82,
                "mean_activation": 0.31,
            },
        }
