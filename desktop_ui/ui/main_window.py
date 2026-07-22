"""Day 9 NeuroFence window: data-driven presentation and navigation layer."""

from desktop_ui.controllers.integration_controller import (
    IntegrationController,
)


from pathlib import Path

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QTimer, Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QPushButton,
    QGraphicsOpacityEffect,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from desktop_ui.components.circular_gauge import CircularGauge
from desktop_ui.controllers.dashboard_controller import DashboardController
from desktop_ui.controllers.scan_controller import ScanController
from desktop_ui.models.scan_result import ScanResult
from desktop_ui.services.dummy_data_service import DummyDataService
from desktop_ui.services.export_service import ExportService
from desktop_ui.services.settings_service import SettingsService
from desktop_ui.components.recent_scan_panel import RecentScanPanel
from desktop_ui.components.system_info import SystemInfo
from desktop_ui.components.system_status_card import SystemStatusCard
from desktop_ui.components.top_bar import TopBar
from desktop_ui.pages.history_page import HistoryPage
from desktop_ui.pages.report_page import ReportPage
from desktop_ui.pages.settings_page import SettingsPage
from desktop_ui.pages.reports_page import ReportsPage
from desktop_ui.widgets.activity_widget import ActivityWidget
from desktop_ui.widgets.info_card import InfoCard
from desktop_ui.widgets.logs_widget import LogsWidget
from desktop_ui.widgets.progress_card import ProgressCard
from desktop_ui.widgets.scan_card import ScanCard
from desktop_ui.widgets.sidebar import Sidebar
from desktop_ui.widgets.upload_card import UploadCard


class MainWindow(QMainWindow):
    """Main responsive dashboard and future backend integration boundary."""

    COMPACT_WIDTH = 1100

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NeuroFence | LLM Weight Poisoning & Backdoor Scanner")
        self.resize(1500, 920)
        self.setMinimumSize(820, 620)

        self._compact_mode: bool | None = None
        self.last_threat_score = 0
        self.last_scan_result = "READY"
        self.latest_scan_result: ScanResult | None = None

        self.settings_service = SettingsService()
        self.app_settings = self.settings_service.load_settings()
        self.export_service = ExportService()
        self.setup_ui()
        self.setup_menu()
        self.data_service = DummyDataService()
        self.scan_controller = ScanController(self.data_service, self)
        self.dashboard_controller = DashboardController(self, self.data_service)
        self.integration_controller = IntegrationController(dashboard_controller=self.dashboard_controller,logs_widget=self.logs_widget,status_callback=self.statusBar().showMessage,)
        self.connect_signals()
        self.update_dashboard("Protected")
        self.statusBar().showMessage("Ready | NeuroFence scanner protected")
        self.apply_settings(self.app_settings, startup=True)
        QTimer.singleShot(0, self._update_responsive_layout)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def setup_ui(self) -> None:
        central_widget = QWidget(self)
        central_widget.setObjectName("mainCentralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        root_layout.addWidget(self.sidebar)

        self.page_stack = QStackedWidget()
        self.page_stack.setObjectName("pageStack")
        root_layout.addWidget(self.page_stack, 1)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("DashboardPage")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.page_stack.addWidget(self.scroll_area)

        self.dashboard_widget = QWidget()
        self.dashboard_widget.setObjectName("dashboardWidget")
        self.scroll_area.setWidget(self.dashboard_widget)
        self.dashboard_layout = QVBoxLayout(self.dashboard_widget)
        self.dashboard_layout.setContentsMargins(28, 28, 28, 28)
        self.dashboard_layout.setSpacing(26)

        self.top_bar = TopBar()
        self.top_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.dashboard_layout.addWidget(self.top_bar)
        self._build_statistics_section()
        self._build_action_section()
        self._build_analysis_section()
        self._build_day6_overview_section()
        self._build_activity_section()

        self.logs_widget = LogsWidget()
        self.logs_widget.setMinimumHeight(230)
        self.logs_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.dashboard_layout.addWidget(self.logs_widget, 1)

        self.reports_page = ReportsPage()
        self.history_page = HistoryPage()
        self.report_page = ReportPage()
        self.settings_page = SettingsPage()
        self.page_stack.addWidget(self.reports_page)
        self.page_stack.addWidget(self.history_page)
        self.page_stack.addWidget(self.report_page)
        self.page_stack.addWidget(self.settings_page)
        self._page_indexes = {"dashboard": 0, "models": 0, "scan": 0, "reports": 1, "history": 2, "report": 3, "settings": 4}
        self._page_animation = None
    def _build_statistics_section(self) -> None:
        self.stats_container = QWidget()
        self.stats_layout = QGridLayout(self.stats_container)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_layout.setHorizontalSpacing(20)
        self.stats_layout.setVerticalSpacing(20)

        self.card_models = InfoCard("Models Loaded", "0", "No model selected")
        self.card_threat = InfoCard("Threat Score", "0%", "Awaiting scan result")
        self.card_duration = InfoCard("Scan Duration", "—", "No completed scan")
        self.card_risk = InfoCard("Risk Level", "Ready", "Scanner standing by")
        self.stat_cards = [self.card_models, self.card_threat, self.card_duration, self.card_risk]

        for card in self.stat_cards:
            card.setObjectName("card")
            card.setMinimumHeight(115)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.dashboard_layout.addWidget(self.stats_container)

    def _build_action_section(self) -> None:
        self.action_splitter = self._new_splitter()
        self.upload_card = UploadCard()
        self.scan_card = ScanCard()
        self.upload_card.setMinimumHeight(210)
        self.scan_card.setMinimumHeight(210)
        self.action_splitter.addWidget(self.upload_card)
        self.action_splitter.addWidget(self.scan_card)
        self.action_splitter.setStretchFactor(0, 3)
        self.action_splitter.setStretchFactor(1, 2)
        self.action_splitter.setSizes([600, 400])
        self.dashboard_layout.addWidget(self.action_splitter)

    def _build_analysis_section(self) -> None:
        self.analysis_splitter = self._new_splitter()
        self.gauge = CircularGauge()
        self.system_info = SystemInfo()
        self.gauge.setMinimumSize(240, 240)
        self.system_info.setMinimumSize(320, 240)
        self.gauge.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.system_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.analysis_splitter.addWidget(self.gauge)
        self.analysis_splitter.addWidget(self.system_info)
        self.analysis_splitter.setStretchFactor(0, 2)
        self.analysis_splitter.setStretchFactor(1, 3)
        self.analysis_splitter.setSizes([400, 600])
        self.dashboard_layout.addWidget(self.analysis_splitter)

    def _build_day6_overview_section(self) -> None:
        self.overview_splitter = self._new_splitter()
        self.recent_scan_panel = RecentScanPanel()
        self.system_status_card = SystemStatusCard()
        self.recent_scan_panel.setMinimumHeight(245)
        self.system_status_card.setMinimumHeight(245)
        self.overview_splitter.addWidget(self.recent_scan_panel)
        self.overview_splitter.addWidget(self.system_status_card)
        self.overview_splitter.setStretchFactor(0, 1)
        self.overview_splitter.setStretchFactor(1, 1)
        self.overview_splitter.setSizes([500, 500])
        self.dashboard_layout.addWidget(self.overview_splitter)

    def _build_activity_section(self) -> None:
        self.activity_splitter = self._new_splitter()
        self.activity = ActivityWidget()
        self.progress_card = ProgressCard()
        self.activity.setMinimumHeight(180)
        self.progress_card.setMinimumHeight(180)
        self.progress_card.setObjectName("card")
        self.activity_splitter.addWidget(self.activity)
        self.activity_splitter.addWidget(self.progress_card)
        self.activity_splitter.setStretchFactor(0, 2)
        self.activity_splitter.setStretchFactor(1, 1)
        self.activity_splitter.setSizes([660, 340])
        self.dashboard_layout.addWidget(self.activity_splitter)

    @staticmethod
    def _new_splitter() -> QSplitter:
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.setHandleWidth(8)
        return splitter

    def _ensure_sidebar_help_action(self) -> None:
        sidebar_layout = self.sidebar.layout()
        if sidebar_layout is None:
            return
        if any(button.text().strip().lower() == "help" for button in self.sidebar.findChildren(QPushButton)):
            return
        help_button = QPushButton("Help")
        help_button.setCursor(Qt.CursorShape.PointingHandCursor)
        help_button.clicked.connect(self.show_about)
        sidebar_layout.insertWidget(max(0, sidebar_layout.count() - 1), help_button)

    def setup_menu(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        tools_menu = self.menuBar().addMenu("Tools")
        help_menu = self.menuBar().addMenu("Help")

        file_menu.addAction("Exit").triggered.connect(self.close)
        tools_menu.addAction("Reset Dashboard").triggered.connect(self.reset_dashboard)
        tools_menu.addAction("Toggle Full Screen").triggered.connect(self.toggle_fullscreen)
        tools_menu.addAction("Display Latest Report").triggered.connect(self.display_report)
        help_menu.addAction("About NeuroFence").triggered.connect(self.show_about)

    def connect_signals(self) -> None:
        self.scan_card.scan_button.clicked.connect(self.run_scan)
        self.upload_card.button.clicked.connect(self.load_model)
        self.sidebar.page_requested.connect(self.navigate_to)
        self.history_page.export_requested.connect(self.export_report)
        self.history_page.filter_requested.connect(self.filter_history)
        self.history_page.search_requested.connect(self.search_history)
        self.report_page.export_json_requested.connect(self.export_json)
        self.report_page.export_csv_requested.connect(self.export_csv)
        self.report_page.export_pdf_requested.connect(self.export_pdf)
        self.report_page.save_requested.connect(self.save_report)
        self.settings_page.save_requested.connect(self.save_settings)
        self.settings_page.reset_requested.connect(self.reset_settings)
        self.settings_page.clear_logs_requested.connect(self.clear_application_logs)

        self.scan_controller.scan_started.connect(self.dashboard_controller.prepare_scan)
        self.scan_controller.stage_changed.connect(self.dashboard_controller.update_stage)
        self.scan_controller.scan_completed.connect(self._handle_scan_completed)
        self.scan_controller.scan_failed.connect(self._handle_scan_error)

    def navigate_to(self, page_name: str) -> None:
        """Open a sidebar page while preserving the dashboard state."""
        if page_name == "help":
            self.show_about()
            self.sidebar.select_page("dashboard" if self.page_stack.currentIndex() == 0 else page_name)
            return
        index = self._page_indexes.get(page_name, 0)
        self.page_stack.setCurrentIndex(index)
        self.sidebar.select_page(page_name)
        if page_name == "models":
            self.scroll_area.verticalScrollBar().setValue(self.upload_card.y())
        elif page_name == "scan":
            self.scroll_area.verticalScrollBar().setValue(self.scan_card.y())
        if self.app_settings.get("general", {}).get("enable_animations", True):
            self._animate_current_page()

    def _animate_current_page(self) -> None:
        page = self.page_stack.currentWidget()
        effect = QGraphicsOpacityEffect(page)
        page.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity", self)
        animation.setDuration(240)
        animation.setStartValue(0.18)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.finished.connect(lambda: page.setGraphicsEffect(None))
        self._page_animation = animation
        animation.start()

    # ------------------------------------------------------------------
    # Responsive layout
    # ------------------------------------------------------------------

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._update_responsive_layout()

    def _update_responsive_layout(self) -> None:
        compact = self.width() < self.COMPACT_WIDTH
        if compact == self._compact_mode:
            return
        self._compact_mode = compact
        self.sidebar.setFixedWidth(175 if compact else 240)

        orientation = Qt.Orientation.Vertical if compact else Qt.Orientation.Horizontal
        for splitter in (
            self.action_splitter,
            self.analysis_splitter,
            self.overview_splitter,
            self.activity_splitter,
        ):
            splitter.setOrientation(orientation)

        self._arrange_stat_cards(compact)
        if compact:
            self.action_splitter.setSizes([220, 220])
            self.analysis_splitter.setSizes([260, 260])
            self.overview_splitter.setSizes([245, 245])
            self.activity_splitter.setSizes([190, 190])
        else:
            self.action_splitter.setSizes([600, 400])
            self.analysis_splitter.setSizes([400, 600])
            self.overview_splitter.setSizes([500, 500])
            self.activity_splitter.setSizes([660, 340])

    def _arrange_stat_cards(self, compact: bool) -> None:
        for card in self.stat_cards:
            self.stats_layout.removeWidget(card)
        if compact:
            for row, card in enumerate(self.stat_cards):
                self.stats_layout.addWidget(card, row, 0)
                self.stats_layout.setRowStretch(row, 1)
            self.stats_layout.setColumnStretch(0, 1)
        else:
            for column, card in enumerate(self.stat_cards):
                self.stats_layout.addWidget(card, 0, column)
                self.stats_layout.setColumnStretch(column, 1)

    # ------------------------------------------------------------------
    # Day 9 data binding and integration boundaries
    # ------------------------------------------------------------------

    def load_model(self) -> None:
        """Publish the selected model through DashboardController."""
        model_path = self.upload_card.model_path
        if model_path:
            self.dashboard_controller.model_selected(model_path)

    def run_scan(self) -> None:
        """Delegate the full scan workflow to ScanController."""
        if self.scan_controller.is_running:
            self.logs_widget.append_log("WARNING", "A scan is already in progress")
            return
        model_path = self.upload_card.model_path

        if not model_path:
            QMessageBox.warning(self, "No Model Selected", "Please select a model first.")
            return
        
        self.logs_widget.append_log("INFO","Starting integration pipeline...")
        self.scan_controller.start_scan(model_path)

    def update_dashboard(self, status: str = "Protected") -> None:
        """Backward-compatible high-level status hook."""
        self.top_bar.set_system_status(status)

    def update_statistics(
        self, *, models_loaded: int | None = None, threat_score: int | None = None,
        duration: float | None = None, risk_level: str | None = None, status: str | None = None,
    ) -> None:
        """Compatibility adapter; Day 9 updates normally flow through DashboardController."""
        if models_loaded is not None:
            self.card_models.update_content(value=str(models_loaded))
        if threat_score is not None:
            self.card_threat.update_content(value=f"{threat_score}%")
        if duration is not None:
            self.card_duration.update_content(value=f"{duration:.1f}s")
        if risk_level is not None:
            self.card_risk.update_content(value=risk_level.title())
        elif status is not None:
            self.card_risk.update_content(value=status)

    def display_report(self) -> None:
        if self.latest_scan_result is None:
            QMessageBox.information(self, "No Scan Report", "Complete a scan before opening the detailed report.")
            return
        self.navigate_to("report")

    def load_scan_history(self) -> None:
        """TODO: load persisted scan records from the future storage backend."""
        self.logs_widget.add_log("Scan history interface refreshed", "INFO")

    def generate_report(self) -> None:
        """TODO: connect persisted report generation/export workflow here."""
        self.navigate_to("reports")

    def refresh_statistics(self) -> None:
        """TODO: calculate aggregates from persisted results later."""
        self.reports_page.threat_statistics.set_statistics(critical=0, medium=2, low=5, safe=17)

    def export_report(self) -> None:
        """Open the detailed report viewer and its export toolbar."""
        self.display_report()

    def build_report(self):
        """Build a normalized report from the latest ScanResult."""
        return self.export_service.build_report(self.latest_scan_result) if self.latest_scan_result else None

    def _require_result(self) -> bool:
        if self.latest_scan_result is None:
            QMessageBox.information(self, "Nothing to Export", "Run a scan before exporting a report.")
            return False
        return True

    def export_json(self) -> None:
        if not self._require_result(): return
        path, _ = QFileDialog.getSaveFileName(self, "Export JSON", "neurofence_report.json", "JSON Files (*.json)")
        if path:
            self.export_service.export_json(self.latest_scan_result, path)
            self.statusBar().showMessage(f"JSON report exported: {path}")

    def export_csv(self) -> None:
        if not self._require_result(): return
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "neurofence_report.csv", "CSV Files (*.csv)")
        if path:
            self.export_service.export_csv(self.latest_scan_result, path)
            self.statusBar().showMessage(f"CSV report exported: {path}")

    def export_pdf(self) -> None:
        if not self._require_result(): return
        QMessageBox.information(self, "PDF Export", "PDF export is prepared for the final renderer after the report format is frozen.")

    def save_report(self) -> None:
        if not self._require_result(): return
        path, _ = QFileDialog.getSaveFileName(self, "Save Report", "neurofence_saved_report.json", "Report Files (*.json)")
        if path:
            self.export_service.save_report(self.latest_scan_result, path)
            self.statusBar().showMessage(f"Report saved: {path}")

    def search_history(self, query: str = "") -> None:
        """Search hook; HistoryTable currently performs local filtering."""
        self.statusBar().showMessage(f"History search: {query or 'all records'}")

    def filter_history(self) -> None:
        """TODO: connect date, score and result filters to persistence later."""
        QMessageBox.information(self, "History Filters", "Advanced history filters will be connected here.")

    def start_scan(self) -> None:
        """Backward-compatible alias retained for older UI code."""
        self.run_scan()

    # ------------------------------------------------------------------
    # Controller event handlers
    # ------------------------------------------------------------------

    def _handle_scan_completed(self, result: ScanResult) -> None:
        if not self.validate_scan_result(result):
            QMessageBox.warning(self, "Validation Error", "Scan result failed validation.")
            return
        self.latest_scan_result = result
        self.last_threat_score = result.threat_score
        self.last_scan_result = result.overall_status
        self.dashboard_controller.bind_scan_result(result)
        self.report_page.set_scan_result(result)
        if self.app_settings.get("general", {}).get("auto_save_reports", False):
            self.logs_widget.append_log("INFO", "Auto-save preference enabled; report is ready for persistence")
        self.refresh_statistics()

    def _handle_scan_error(self, module: str, message: str) -> None:
        self.logs_widget.append_log("ERROR", f"{module}: {message}")
        self.statusBar().showMessage(f"Error: {module}")
        QMessageBox.warning(
            self,
            f"{module} Error",
            message,
        )

    # ------------------------------------------------------------------
    # Shared helpers and window actions
    # ------------------------------------------------------------------

    @staticmethod
    def _set_info_card_value(card: InfoCard, value: str) -> None:
        if hasattr(card, "set_value"):
            card.set_value(value)
            return
        label = card.findChild(QLabel, "cardValue")
        if label is not None:
            label.setText(value)

    def card_status_value(self, status: str) -> None:
        self.card_risk.update_content(value=status)

    def _current_model_name(self) -> str:
        if not self.upload_card.model_path:
            return "Demo Model"
        return Path(self.upload_card.model_path).name or "Selected Model"

    def reset_dashboard(self) -> None:
        self.scan_controller.cancel_scan()
        self.latest_scan_result = None
        if hasattr(self, "report_page"):
            self.report_page.clear_report()
        self.scan_card.scan_button.setEnabled(True)
        self.scan_card.status.setText("●  Ready for analysis")
        self.progress_card.reset_progress()
        self.gauge.setValue(0)
        self.activity.clear_entries()
        self.activity.append_entry("NeuroFence initialized")
        self.activity.append_entry("Waiting for model")
        self.logs_widget.clear_logs()
        self.logs_widget.append_log("INFO", "NeuroFence initialized")
        self.logs_widget.append_log("INFO", "Waiting for model upload")
        self.logs_widget.append_log("SUCCESS", "Scanner ready")
        self.recent_scan_panel.reset()
        self.system_status_card.set_scanner_status("Ready", "normal")
        self.card_models.update_content(value="1" if self.upload_card.model_path else "0", subtitle="Ready" if self.upload_card.model_path else "No model selected")
        self.card_threat.update_content(value="0%", subtitle="Awaiting scan result")
        self.card_duration.update_content(value="—", subtitle="No completed scan")
        self.card_risk.update_content(value="Ready", subtitle="Scanner standing by")
        self.update_dashboard("Protected")
        self.statusBar().showMessage("Dashboard reset | Ready")

    def save_settings(self, settings: dict) -> None:
        self.settings_service.save_settings(settings)
        self.app_settings = settings
        self.apply_settings(settings)
        self.logs_widget.append_log("SUCCESS", "Application settings saved")
        self.statusBar().showMessage("Settings saved and applied")

    def reset_settings(self) -> None:
        settings = self.settings_service.reset_to_defaults()
        self.settings_page.set_settings(settings)
        self.app_settings = settings
        self.apply_settings(settings)
        self.statusBar().showMessage("Settings reset to defaults")

    def apply_settings(self, settings: dict, startup: bool = False) -> None:
        self.settings_page.set_settings(settings)
        font_size = int(settings.get("appearance", {}).get("font_size", 11))
        font = self.font(); font.setPointSize(font_size); self.setFont(font)
        max_logs = int(settings.get("logging", {}).get("maximum_log_entries", 500))
        if hasattr(self.logs_widget, "console"):
            self.logs_widget.console.document().setMaximumBlockCount(max_logs)
        if startup and settings.get("general", {}).get("start_maximized", False):
            QTimer.singleShot(0, self.showMaximized)

    def clear_application_logs(self) -> None:
        self.logs_widget.clear_logs()
        self.logs_widget.append_log("INFO", "Logs cleared from Settings")
        self.statusBar().showMessage("Application logs cleared")
    
    
    def toggle_fullscreen(self) -> None:
        self.showNormal() if self.isFullScreen() else self.showFullScreen()

    def get_model_loader(self):
        """
        Day 13 integration hook
        Tanvi's Model Loader
        """
        return None

    def get_detection_service(self):
        """
        Day 13 integration hook
        Dhruti's Detection Service
        """
        return None

    def get_activation_tracker(self):
        """
        Day 13 integration hook
        Akhina's Activation Tracker
        """
        return None 

    def validate_scan_result(self,result,) -> bool:
        if result is None:
            return False
        required = [
            "model_name",
            "framework",
            "architecture",
            "threat_score",
            "risk_level",
            "scan_duration",]
        for field in required:
            if not hasattr(result, field):
                self.logs_widget.append_log("ERROR",f"Missing field: {field}")
                return False
        return True
     
    def show_about(self) -> None:
        QMessageBox.about(
            self,
            "About NeuroFence",
            (
                "<b>NeuroFence v1.1</b><br><br>"
                "A desktop security platform for detecting model poisoning, backdoors, "
                "suspicious prompts and abnormal neural activations.<br><br>"
                "<b>Team responsibilities</b><br>"
                "Harshi — Desktop UI, orchestration, reports and configuration<br>"
                "Tanvi — Model Loader and metadata<br>"
                "Dhruti — Detection and prompt fuzzing<br>"
                "Akhina — Activation tracking and neuron analysis<br><br>"
                "Developed as part of the internship project using Python and PyQt6."
            ),
        )
