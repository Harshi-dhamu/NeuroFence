"""Day 9 non-blocking scan workflow driven by a common ScanResult model."""
from __future__ import annotations

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from desktop_ui.models.scan_result import ScanResult
from desktop_ui.services.dummy_data_service import DummyDataService


class ScanController(QObject):
    scan_started = pyqtSignal(str)
    stage_changed = pyqtSignal(int, int, str, str, str)
    scan_completed = pyqtSignal(object)
    scan_failed = pyqtSignal(str, str)
    scan_state_changed = pyqtSignal(str)

    STAGES = (
        (6, "Initialize scanner", "Initializing data-driven scan controller"),
        (17, "Load model information", "Retrieving normalized model metadata"),
        (29, "Validate model structure", "Validating architecture and model package"),
        (44, "Run detection", "Retrieving Detection & Fuzzing results"),
        (59, "Track activations", "Retrieving activation and neuron analysis"),
        (72, "Normalize results", "Building the common ScanResult model"),
        (84, "Bind dashboard", "Publishing values to dashboard widgets"),
        (94, "Update reports", "Synchronizing report and history views"),
        (100, "Complete scan", "Data-driven scan completed successfully"),
    )

    def __init__(self, data_service: DummyDataService | None = None, parent=None) -> None:
        super().__init__(parent)
        self.data_service = data_service or DummyDataService()
        self.timer = QTimer(self)
        self.timer.setInterval(520)
        self.timer.timeout.connect(self._advance)
        self._model_path = ""
        self._stage_index = 0
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
        try:
            # Future replacement point: real Model/Detection/Activation providers.
            self._result = self.data_service.get_scan_result(model_path)
        except Exception as exc:
            self.scan_failed.emit("Dummy Data Service", str(exc))
            return
        self.scan_state_changed.emit("SCANNING")
        self.scan_started.emit(model_path)
        self.timer.start()

    def cancel_scan(self) -> None:
        self.timer.stop()
        self.scan_state_changed.emit("READY")

    def _advance(self) -> None:
        if self._result is None:
            self.timer.stop()
            self.scan_failed.emit("Scan Controller", "No scan result was produced.")
            return
        if self._stage_index >= len(self.STAGES):
            self.timer.stop()
            self.scan_state_changed.emit(self._result.overall_status)
            self.scan_completed.emit(self._result)
            return
        progress, stage, message = self.STAGES[self._stage_index]
        target = self._result.threat_score
        threat = min(target, round(target * progress / 100))
        level = "SUCCESS" if progress == 100 else "INFO"
        self.stage_changed.emit(progress, threat, stage, message, level)
        self._stage_index += 1
