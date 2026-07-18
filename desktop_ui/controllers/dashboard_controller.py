"""Central data-binding controller for every NeuroFence dashboard widget."""
from __future__ import annotations

from pathlib import Path

from desktop_ui.models.scan_result import ScanResult
from desktop_ui.services.dummy_data_service import DummyDataService


class DashboardController:
    """Own widget updates so MainWindow contains no presentation plumbing."""

    def __init__(self, window, data_service: DummyDataService | None = None) -> None:
        self.window = window
        self.data_service = data_service or DummyDataService()
        self.models_loaded = 0
        self.last_result: ScanResult | None = None

    def model_selected(self, model_path: str) -> None:
        name = Path(model_path).name or "Selected Model"
        self.models_loaded = 1
        self.window.card_models.update_content(value="1", subtitle=f"Ready: {name}")
        self.window.activity.append_entry(f"Model selected: {name}")
        self.window.logs_widget.append_log("INFO", f"Model selected and ready: {name}")
        self.window.statusBar().showMessage(f"Ready | Model: {name}")

    def prepare_scan(self, model_path: str) -> None:
        name = Path(model_path).name or "Selected Model"
        w = self.window
        w.logs_widget.clear_logs()
        w.activity.clear_entries()
        w.progress_card.update_progress(0, "Initializing scan pipeline")
        w.gauge.setValue(0)
        w.scan_card.status.setText("●  Data pipeline active")
        w.scan_card.scan_button.setEnabled(False)
        w.recent_scan_panel.set_result("SCANNING")
        w.system_status_card.set_scanner_status("Scanning", "scanning")
        w.top_bar.set_system_status("Scanning")
        w.card_models.update_content(value=str(max(1, self.models_loaded)), subtitle=name)
        w.card_threat.update_content(value="0%", subtitle="Analysis in progress")
        w.card_duration.update_content(value="—", subtitle="Calculating elapsed time")
        w.card_risk.update_content(value="Scanning", subtitle="Awaiting detection results")
        w.logs_widget.append_log("INFO", f"Dummy data provider accepted: {name}")
        w.activity.append_entry("Data-driven scan started")
        w.statusBar().showMessage(f"Scanning {name}...")

    def update_stage(self, progress: int, threat: int, stage: str, message: str, level: str) -> None:
        w = self.window
        w.progress_card.update_progress(progress, stage)
        w.gauge.setValue(threat)
        w.activity.append_entry(stage)
        w.logs_widget.append_log(level, message)
        w.card_threat.update_content(value=f"{threat}%", subtitle=f"Current stage: {stage}")
        w.statusBar().showMessage(f"Scanning | {progress}% | {stage}")

    def bind_scan_result(self, result: ScanResult) -> None:
        """Bind one common model to dashboard, reports, history and status UI."""
        self.last_result = result
        self.models_loaded = max(1, self.models_loaded)
        w = self.window
        state = "normal" if result.overall_status == "SAFE" else "warning"

        w.progress_card.update_progress(100, f"Scan completed — {result.overall_status}")
        w.gauge.setValue(result.threat_score)
        w.scan_card.scan_button.setEnabled(True)
        w.scan_card.status.setText(f"●  {result.overall_status} — data binding complete")
        w.system_status_card.set_scanner_status(result.overall_status, state)
        w.top_bar.set_system_status("Protected" if result.overall_status == "SAFE" else "Warning")

        w.card_models.update_content(value=str(self.models_loaded), subtitle=result.model_name)
        w.card_threat.update_content(value=f"{result.threat_score}%", subtitle="Latest normalized score")
        w.card_duration.update_content(value=f"{result.scan_duration:.1f}s", subtitle="Latest scan duration")
        w.card_risk.update_content(value=result.risk_level.title(), subtitle=result.overall_status)

        w.recent_scan_panel.update_scan(
            scan_time=result.timestamp, model_name=result.model_name,
            threat_score=result.threat_score, duration_seconds=result.scan_duration,
            result=result.overall_status,
        )
        w.logs_widget.append_log("SUCCESS", result.detection_summary)
        w.logs_widget.append_log("SAFE" if result.overall_status == "SAFE" else "WARNING", result.activation_summary)
        w.logs_widget.append_log("SUCCESS", "Common ScanResult bound to all dashboard widgets")
        w.activity.append_entry("Dashboard, report and history synchronized")

        w.reports_page.update_latest_report(
            result.model_name, result.overall_status, result.threat_score,
            result.scan_duration, result.timestamp, result.recommendation,
        )
        w.history_page.history_table.add_scan(
            f"NF-{w.history_page.history_table.rowCount() + 20:04d}",
            result.model_name, result.timestamp, f"{result.threat_score}%", result.overall_status,
        )
        w.statusBar().showMessage(
            f"Ready | Last Scan: {result.timestamp.split(',')[-1].strip()} | "
            f"Risk Level: {result.risk_level.title()} | Framework: {result.framework}"
        )

    def display_error(self, module: str, message: str) -> None:
        w = self.window
        w.scan_card.scan_button.setEnabled(True)
        w.scan_card.status.setText("●  Scan failed — review logs")
        w.progress_card.update_progress(0, "Scan interrupted")
        w.system_status_card.set_scanner_status("Error", "critical")
        w.top_bar.set_system_status("Warning")
        w.card_risk.update_content(value="Error", subtitle=module)
        w.logs_widget.append_log("ERROR", f"{module}: {message}")
        w.activity.append_entry(f"{module} failed")
        w.statusBar().showMessage(f"Error | {module}: {message}")

    # Integration hooks: swap DummyDataService calls for teammate APIs later.
    def load_model_information(self, model_path: str) -> ScanResult:
        return self.data_service.get_scan_result(model_path)

    def retrieve_detection_results(self, result: ScanResult):
        return result.detection

    def retrieve_activation_analysis(self, result: ScanResult):
        return result.activation
