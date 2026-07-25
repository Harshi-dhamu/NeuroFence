from __future__ import annotations

import time

from desktop_ui.services.integration_service import (
    IntegrationService,
)

from desktop_ui.validators.result_validator import (
    ResultValidator,
)

from desktop_ui.services.model_service import (
    ModelService,
)

from desktop_ui.services.detection_service import (
    DetectionService,
)

from desktop_ui.services.activation_service import (
    ActivationService,
)

from desktop_ui.models.scan_result import (
    ScanResult,
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

    def log(
        self,
        level,
        message,
    ):
        if self.logs_widget:
            self.logs_widget.append_log(
                level,
                message,
            )

    def set_status(
        self,
        text,
    ):
        if self.status_callback:
            self.status_callback(text)

    def execute_scan_pipeline(
        self,
        model_path=None,
    ):

        start_time = time.time()

        try:

            self.set_status(
                "Loading Model..."
            )

            self.log(
                "INFO",
                "Starting model loading",
            )

            load_result = (
                self.model_service.load_model(
                    model_path
                )
            )

            self.log(
                "INFO",
                f"Load Result: {load_result}",
            )

            self.set_status(
                "Validating Model..."
            )

            validated = (
                self.model_service.validate_model()
            )

            if not validated:

                self.log(
                    "ERROR",
                    "Model validation failed",
                )

                raise ValueError(
                    "Model validation failed"
                )

            self.log(
                "SUCCESS",
                "Model validation passed",
            )

            model_info = (
                self.model_service.get_model_info()
            )

            self.set_status(
                "Running Detection..."
            )

            self.log(
                "INFO",
                "Starting detection engine",
            )

            detection = (
                self.detection_service.run_detection(
                    "security scan"
                )
            )

            self.log(
                "SUCCESS",
                "Detection completed",
            )

            activation = {}

            try:

                self.set_status(
                    "Running Activation Tracking..."
                )

                self.log(
                    "INFO",
                    "Starting activation analysis",
                )

                activation = (
                    self.activation_service.analyze(
                        self.model_service.loader
                    )
                )

                self.log(
                    "SUCCESS",
                    "Activation analysis completed",
                )

            except Exception as exc:

                activation = {
                    "statistics": {},
                    "error": str(exc),
                }

                self.log(
                    "WARNING",
                    f"Activation analysis failed: {exc}",
                )

            self.set_status(
                "Generating Report..."
            )

            result = ScanResult()

            # -----------------------------
            # Model Information
            # -----------------------------

            result.model.model_name = (
                model_info
                .get(
                    "model_identity",
                    {},
                )
                .get(
                    "name",
                    "Unknown Model",
                )
            )

            result.model.model_path = (
                model_info
                .get(
                    "model_identity",
                    {},
                )
                .get(
                    "local_path",
                    "",
                )
            )

            result.model.framework = (
                model_info
                .get(
                    "tensor_properties",
                    {},
                )
                .get(
                    "framework",
                    "Unknown",
                )
            )

            result.model.architecture = (
                model_info
                .get(
                    "architecture_details",
                    {},
                )
                .get(
                    "architecture",
                    "Unknown",
                )
            )

            result.model.layers = (
                model_info
                .get(
                    "architecture_details",
                    {},
                )
                .get(
                    "layers_count",
                    0,
                )
            )

            # -----------------------------
            # Detection Results
            # -----------------------------

            result.detection.threat_score = (
                detection.get(
                    "score",
                    0,
                )
            )

            result.detection.risk_level = (
                detection.get(
                    "risk_level",
                    "Unknown",
                )
            )

            result.detection.summary = str(
                detection.get(
                    "report",
                    {},
                )
            )

            recommendations = (
                detection
                .get(
                    "report",
                    {},
                )
                .get(
                    "Recommendations",
                    [],
                )
            )

            result.detection.suspicious_prompts = (
                recommendations
            )

            # -----------------------------
            # Activation Results
            # -----------------------------

            statistics = (
                activation.get(
                    "statistics",
                    {},
                )
            )

            result.activation.neuron_information = (
                statistics
            )

            result.activation.summary = (
                f"{len(statistics)} layers analyzed"
            )

            result.activation.neurons_analyzed = (
                len(statistics)
            )

            # -----------------------------
            # Recommendation
            # -----------------------------

            if recommendations:

                result.recommendation = (
                    "\n".join(
                        recommendations
                    )
                )

            else:

                result.recommendation = (
                    "No recommendation available."
                )

            # -----------------------------
            # Statistics
            # -----------------------------

            duration = round(
                time.time() - start_time,
                2,
            )

            result.statistics.duration_seconds = (
                duration
            )

            result.statistics.stages_completed = (
                7
            )

            result.statistics.overall_status = (
                "SUCCESS"
            )

            # -----------------------------
            # Validation
            # -----------------------------

            validator = ResultValidator()

            if hasattr(
                validator,
                "validate",
            ):
                validator.validate(
                    result
                )

            self.set_status(
                "Scan Completed"
            )

            self.log(
                "SUCCESS",
                f"Scan completed in {duration} seconds",
            )

            return result

        except Exception as exc:

            self.log(
                "ERROR",
                str(exc),
            )

            self.set_status(
                "Scan Failed"
            )

            raise