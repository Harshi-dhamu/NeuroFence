"""Presentation adapter that keeps repetitive widget updates out of MainWindow."""
from __future__ import annotations

from pathlib import Path

from desktop_ui.controllers.integration import ScanResult


class UIController:
    """Apply controller events to the existing NeuroFence widgets."""

    def __init__(self, window) -> None:
        self.window = window

    def prepare_scan(self, model_path: str) -> None:
        w = self.window
        model_name = Path(model_path).name or "Selected Model"
        w.logs_widget.clear_logs()
        w.activity.list.clear()
        w.progress_card.progress.setValue(0)
        w.progress_card.set_stage("Initializing scan pipeline")
        w.gauge.setValue(0)
        w.scan_card.status.setText("●  Backend pipeline active")
        w.scan_card.scan_button.setEnabled(False)
        w.recent_scan_panel.set_result("SCANNING")
        w.system_status_card.set_scanner_status("Scanning", "scanning")
        w.update_dashboard("Scanning")
        w.update_statistics(models_loaded=1, threat_score=0, status="Scanning")
        w.logs_widget.add_log(f"Controller accepted model: {model_name}", "INFO")
        w.statusBar().showMessage("Scan controller started")

    def update_stage(self, progress: int, threat: int, stage: str, message: str, level: str) -> None:
        w = self.window
        w.progress_card.progress.setValue(progress)
        w.progress_card.set_stage(stage)
        w.gauge.setValue(threat)
        w.activity.add_activity(stage)
        w.logs_widget.add_log(message, level)
        w.update_statistics(threat_score=threat, status="Scanning")
        w.statusBar().showMessage(f"{progress}% | {stage}")

    def display_result(self, result: ScanResult) -> None:
        w = self.window
        w.progress_card.progress.setValue(100)
        w.progress_card.set_stage(f"Scan completed — {result.overall_status}")
        w.gauge.setValue(result.threat_score)
        w.scan_card.scan_button.setEnabled(True)
        w.scan_card.status.setText(f"●  {result.overall_status} — pipeline completed")
        state = "normal" if result.overall_status == "SAFE" else "warning"
        w.system_status_card.set_scanner_status(result.overall_status, state)
        w.recent_scan_panel.update_scan(
            scan_time=result.timestamp,
            model_name=result.model_name,
            threat_score=result.threat_score,
            duration_seconds=result.scan_duration,
            result=result.overall_status,
        )
        w.logs_widget.add_log(result.detection_summary, "SUCCESS")
        w.logs_widget.add_log(result.activation_summary, "SAFE")
        w.logs_widget.add_log("All module results collected successfully", "SUCCESS")
        w.activity.add_activity("Report and history updated")
        w.update_dashboard("Protected" if result.overall_status == "SAFE" else "Warning")
        w.update_statistics(models_loaded=1, threat_score=result.threat_score, status=result.overall_status)
        w.statusBar().showMessage(
            f"Scan complete | {result.overall_status} | Threat score {result.threat_score}%"
        )

    def display_error(self, module: str, message: str) -> None:
        w = self.window
        w.scan_card.scan_button.setEnabled(True)
        w.scan_card.status.setText("●  Scan failed — review logs")
        w.system_status_card.set_scanner_status("Error", "critical")
        w.update_dashboard("Warning")
        w.update_statistics(status="Error")
        w.logs_widget.add_log(f"{module}: {message}", "ERROR")
        w.activity.add_activity(f"{module} failed")
        w.statusBar().showMessage(f"{module} error: {message}")
