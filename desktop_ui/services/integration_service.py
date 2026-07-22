from __future__ import annotations

from desktop_ui.services.dummy_data_service import DummyDataService


class IntegrationService:
    """
    Day 12 integration-ready service layer.

    Day 13:
    Replace DummyDataService calls with
    ModelService,
    DetectionService,
    ActivationService.
    """

    def __init__(self):
        self.dummy = DummyDataService()

    def load_model(self, model_path):
        return {
            "path": model_path,
            "loaded": True,
        }

    def run_detection(self, model_info):
        result = self.dummy.generate_scan_result()

        return {
            "threat_score": result.threat_score,
            "risk_level": result.risk_level,
            "summary": result.detection_summary,
        }

    def run_activation_tracker(self, model_info):
        result = self.dummy.generate_scan_result()

        return {
            "dead_neurons": result.activation.dead_neurons,
            "anomalous_activations":
            result.activation.anomalous_activations,
            "summary": result.activation_summary,
        }

    def get_complete_result(self):
        return self.dummy.generate_scan_result()