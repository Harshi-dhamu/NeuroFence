from __future__ import annotations
from unittest import result

from desktop_ui.services.integration_service import (
    IntegrationService,
)

from desktop_ui.validators.result_validator import (
    ResultValidator,
)

from desktop_ui.services.model_service import (
    ModelService
)

from desktop_ui.services.detection_service import (
    DetectionService
)

from desktop_ui.services.activation_service import (
    ActivationService
)

from desktop_ui.models.scan_result import (
    ScanResult
)

class IntegrationController:
    def __init__(
        self,
        dashboard_controller=None,
        logs_widget=None,
        status_callback=None,
    ):
        self.model_service = ModelService()
        self.detection_service = DetectionService()
        self.activation_service = ActivationService()

        self.service = IntegrationService()

        self.dashboard_controller = dashboard_controller
        self.logs_widget = logs_widget
        self.status_callback = status_callback

    def log(self, level, message):
        if self.logs_widget:
            self.logs_widget.append_log(level, message)

    def set_status(self, text):
        if self.status_callback:
            self.status_callback(text)

    def execute_scan_pipeline(
        self,
        model_path=None,
    ):
        load_result = self.model_service.load_model(model_path)
        validated = self.model_service.validate_model()
        if not validated:
            raise ValueError("Model validation failed")
        model_info = self.model_service.get_model_info()
        detection = self.detection_service.run_detection("security scan")
        activation = self.activation_service.analyze(self.model_service.loader)
        result = ScanResult()
        result.model_name = (
            model_info["model_identity"]["name"]
            )
        result.framework = (
            model_info["tensor_properties"]["framework"]
            )
        result.architecture = (
            model_info["architecture_details"]["architecture"]
            )
        result.layers = (
            model_info["architecture_details"]["layers_count"]
            )
        result.threat_score = detection["score"]
        result.risk_level = detection["risk_level"]
        result.activation_summary = (
            f"{len(activation['statistics'])} layers analyzed"
            )
        result.detection_summary = str(
            detection["report"]
            )
        result.overall_status = "SAFE"
        return result
        