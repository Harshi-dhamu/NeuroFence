from __future__ import annotations

from desktop_ui.services.integration_service import (
    IntegrationService,
)

from desktop_ui.validators.result_validator import (
    ResultValidator,
)


class IntegrationController:
    def __init__(
        self,
        dashboard_controller=None,
        logs_widget=None,
        status_callback=None,
    ):
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
        try:
            self.set_status("Loading model...")
            self.log("INFO", "Loading model")

            model_info = self.service.load_model(model_path)

            self.set_status("Running detection...")
            self.log("INFO", "Running detection")

            self.service.run_detection(model_info)

            self.set_status("Running activation tracking...")
            self.log(
                "INFO",
                "Running activation tracker"
            )

            self.service.run_activation_tracker(
                model_info
            )

            result = (
                self.service.get_complete_result()
            )

            errors = (
                ResultValidator.validate(result)
            )

            if errors:
                raise ValueError(
                    "\n".join(errors)
                )

            self.log(
                "SUCCESS",
                "Scan pipeline completed"
            )

            self.set_status(
                "Scan completed successfully."
            )

            return result

        except Exception as exc:
            self.log(
                "ERROR",
                str(exc)
            )

            self.set_status(
                "Scan failed."
            )

            raise