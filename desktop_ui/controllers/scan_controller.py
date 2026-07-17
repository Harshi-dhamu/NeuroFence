"""Non-blocking scan orchestration controller for NeuroFence."""
from __future__ import annotations

from time import perf_counter

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from desktop_ui.controllers.integration import IntegrationBridge, ScanResult


class ScanController(QObject):
    """Coordinate services and publish UI-safe scan events."""

    scan_started = pyqtSignal(str)
    stage_changed = pyqtSignal(int, int, str, str, str)
    scan_completed = pyqtSignal(object)
    scan_failed = pyqtSignal(str, str)
    scan_state_changed = pyqtSignal(str)

    STAGES = (
        (5, "Initialize scanner", "Initializing controller and integration bridge"),
        (16, "Load model", "Loading model through Model Service"),
        (27, "Validate model", "Validating model structure and metadata"),
        (45, "Run detection", "Running Detection & Fuzzing service"),
        (62, "Track activations", "Running Activation Tracker service"),
        (75, "Collect results", "Collecting normalized module outputs"),
        (88, "Generate report", "Generating common scan result"),
        (96, "Update UI", "Publishing scan result to dashboard"),
        (100, "Complete scan", "Backend communication simulation completed"),
    )

    def __init__(self, integration: IntegrationBridge | None = None, parent=None) -> None:
        super().__init__(parent)
        self.integration = integration or IntegrationBridge()
        self.timer = QTimer(self)
        self.timer.setInterval(600)
        self.timer.timeout.connect(self._advance)
        self._model_path = ""
        self._stage_index = 0
        self._started_at = 0.0
        self._model_info: dict[str, object] = {}
        self._detection: dict[str, object] = {}
        self._activation: dict[str, object] = {}
        self._result: ScanResult | None = None

    @property
    def is_running(self) -> bool:
        return self.timer.isActive()

    def start_scan(self, model_path: str) -> None:
        if self.is_running:
            return
        if not model_path:
            self.scan_failed.emit("Model Selection", "Select a model directory before starting the scan.")
            return

        self._model_path = model_path
        self._stage_index = 0
        self._started_at = perf_counter()
        self._model_info = {}
        self._detection = {}
        self._activation = {}
        self._result = None
        self.scan_state_changed.emit("SCANNING")
        self.scan_started.emit(model_path)
        self.timer.start()

    def cancel_scan(self) -> None:
        self.timer.stop()
        self.scan_state_changed.emit("READY")

    def _advance(self) -> None:
        if self._stage_index >= len(self.STAGES):
            self.timer.stop()
            if self._result is not None:
                self.scan_state_changed.emit(self._result.overall_status)
                self.scan_completed.emit(self._result)
            return

        progress, stage, message = self.STAGES[self._stage_index]
        try:
            self._execute_stage(stage)
        except Exception as exc:  # services normalize their own errors
            self.timer.stop()
            module = self._module_for_stage(stage)
            self.scan_state_changed.emit("ERROR")
            self.scan_failed.emit(module, str(exc))
            return

        threat_score = int(self._detection.get("threat_score", 0))
        level = "SUCCESS" if progress == 100 else "INFO"
        self.stage_changed.emit(progress, threat_score, stage, message, level)
        self._stage_index += 1

    def _execute_stage(self, stage: str) -> None:
        if stage == "Load model":
            self._model_info = self.integration.load_model(self._model_path)
        elif stage == "Validate model":
            self.integration.validate_model(self._model_info)
        elif stage == "Run detection":
            self._detection = self.integration.run_detection(self._model_info)
        elif stage == "Track activations":
            self._activation = self.integration.run_activation_tracker(self._model_info)
        elif stage == "Generate report":
            duration = max(0.1, perf_counter() - self._started_at)
            self._result = self.integration.generate_report(
                self._model_info, self._detection, self._activation, duration
            )

    @staticmethod
    def _module_for_stage(stage: str) -> str:
        if stage in {"Load model", "Validate model"}:
            return "Model Loader"
        if stage == "Run detection":
            return "Detection & Fuzzing"
        if stage == "Track activations":
            return "Activation Tracker"
        return "Scan Controller"
