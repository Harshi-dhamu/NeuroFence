"""Day 8 NeuroFence window: presentation layer for controller-driven scans."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QTimer, Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
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
from desktop_ui.controllers.integration import IntegrationBridge, ScanResult
from desktop_ui.controllers.scan_controller import ScanController
from desktop_ui.controllers.ui_controller import UIController
from desktop_ui.components.recent_scan_panel import RecentScanPanel
from desktop_ui.components.system_info import SystemInfo
from desktop_ui.components.system_status_card import SystemStatusCard
from desktop_ui.components.top_bar import TopBar
from desktop_ui.pages.history_page import HistoryPage
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

        self.setup_ui()
        self.setup_menu()
        self.integration = IntegrationBridge()
        self.scan_controller = ScanController(self.integration, self)
        self.ui_controller = UIController(self)
        self.connect_signals()
        self.update_dashboard("Protected")
        self.statusBar().showMessage("Ready | NeuroFence scanner protected")
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
        self.page_stack.addWidget(self.reports_page)
        self.page_stack.addWidget(self.history_page)
        self._page_indexes = {"dashboard": 0, "models": 0, "scan": 0, "reports": 1, "history": 2}
        self._page_animation = None
    def _build_statistics_section(self) -> None:
        self.stats_container = QWidget()
        self.stats_layout = QGridLayout(self.stats_container)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_layout.setHorizontalSpacing(24)
        self.stats_layout.setVerticalSpacing(24)

        self.card_models = InfoCard("Models Loaded", "0", "Models prepared for inspection")
        self.card_threat = InfoCard("Threat Score", "0%", "Current model risk level")
        self.card_status = InfoCard("System Status", "Protected", "Scanner protection state")
        self.stat_cards = [self.card_models, self.card_threat, self.card_status]

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

        self.scan_controller.scan_started.connect(self.ui_controller.prepare_scan)
        self.scan_controller.stage_changed.connect(self.ui_controller.update_stage)
        self.scan_controller.scan_completed.connect(self._handle_scan_completed)
        self.scan_controller.scan_failed.connect(self._handle_scan_error)

    def navigate_to(self, page_name: str) -> None:
        """Open a sidebar page while preserving the dashboard state."""
        if page_name == "help":
            self.show_about()
            self.sidebar.select_page("dashboard" if self.page_stack.currentIndex() == 0 else page_name)
            return
        if page_name == "settings":
            QMessageBox.information(self, "Settings", "Settings page integration is prepared for a future sprint.")
            return
        index = self._page_indexes.get(page_name, 0)
        self.page_stack.setCurrentIndex(index)
        self.sidebar.select_page(page_name)
        if page_name == "models":
            self.scroll_area.verticalScrollBar().setValue(self.upload_card.y())
        elif page_name == "scan":
            self.scroll_area.verticalScrollBar().setValue(self.scan_card.y())
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
    # Day 8 controller and integration boundaries
    # ------------------------------------------------------------------

    def load_model(self) -> None:
        """Reflect the model selected by UploadCard in the dashboard.

        Actual metadata loading is delegated to ModelService when a scan starts.
        """
        model_path = self.upload_card.model_path
        if not model_path:
            return
        model_name = Path(model_path).name or model_path
        self._set_info_card_value(self.card_models, "1")
        self.activity.add_activity(f"Model selected: {model_name}")
        self.logs_widget.add_log(f"Model selected and ready: {model_name}", "INFO")
        self.statusBar().showMessage(f"Model ready: {model_name}")
        self.update_statistics(models_loaded=1)

    def run_scan(self) -> None:
        """Delegate the full scan workflow to ScanController."""
        if self.scan_controller.is_running:
            self.logs_widget.add_log("A scan is already in progress", "WARNING")
            return
        self.scan_controller.start_scan(self.upload_card.model_path)

    def update_dashboard(self, status: str = "Protected") -> None:
        """Update high-level dashboard state from controller events."""
        self.top_bar.set_system_status(status)
        self.card_status_value(status)

    def update_statistics(
        self,
        *,
        models_loaded: int | None = None,
        threat_score: int | None = None,
        status: str | None = None,
    ) -> None:
        """Central publication point for normalized backend statistics."""
        if models_loaded is not None:
            self._set_info_card_value(self.card_models, str(models_loaded))
        if threat_score is not None:
            self._set_info_card_value(self.card_threat, f"{threat_score}%")
        if status is not None:
            self._set_info_card_value(self.card_status, status)

    def display_report(self) -> None:
        self.navigate_to("reports")

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
        """TODO: call IntegrationBridge.export_results and a file writer later."""
        if self.latest_scan_result is None:
            QMessageBox.information(self, "Nothing to Export", "Run a scan before exporting a report.")
            return
        QMessageBox.information(
            self,
            "Export Prepared",
            "The normalized scan result is ready for PDF, JSON or CSV export integration.",
        )

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
        self.latest_scan_result = result
        self.last_threat_score = result.threat_score
        self.last_scan_result = result.overall_status
        self.ui_controller.display_result(result)

        self.reports_page.update_latest_report(
            result.model_name,
            result.overall_status,
            result.threat_score,
            result.scan_duration,
            result.timestamp,
            result.recommendation,
        )
        self.history_page.history_table.add_scan(
            f"NF-{self.history_page.history_table.rowCount() + 20:04d}",
            result.model_name,
            result.timestamp,
            f"{result.threat_score}%",
            result.overall_status,
        )
        self.refresh_statistics()

    def _handle_scan_error(self, module: str, message: str) -> None:
        self.ui_controller.display_error(module, message)
        QMessageBox.warning(
            self,
            f"{module} Error",
            f"The scan could not continue.\n\n{message}\n\nCheck the selected model and try again.",
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
        self._set_info_card_value(self.card_status, status)

    def _current_model_name(self) -> str:
        if not self.upload_card.model_path:
            return "Demo Model"
        return Path(self.upload_card.model_path).name or "Selected Model"

    def reset_dashboard(self) -> None:
        self.scan_controller.cancel_scan()
        self.latest_scan_result = None
        self.scan_card.scan_button.setEnabled(True)
        self.scan_card.status.setText("●  Ready for analysis")
        self.progress_card.progress.setValue(0)
        if hasattr(self.progress_card, "set_stage"):
            self.progress_card.set_stage("Ready to scan")
        self.gauge.setValue(0)
        self.activity.list.clear()
        self.activity.add_activity("NeuroFence initialized")
        self.activity.add_activity("Waiting for model")
        self.logs_widget.clear_logs()
        self.logs_widget.add_log("NeuroFence initialized", "INFO")
        self.logs_widget.add_log("Waiting for model upload", "INFO")
        self.logs_widget.add_log("Scanner ready", "SUCCESS")
        self.recent_scan_panel.reset()
        self.system_status_card.set_scanner_status("Ready", "normal")
        self.update_statistics(
            models_loaded=1 if self.upload_card.model_path else 0,
            threat_score=0,
            status="Protected",
        )
        self.update_dashboard("Protected")
        self.statusBar().showMessage("Dashboard reset | Ready")

    def toggle_fullscreen(self) -> None:
        self.showNormal() if self.isFullScreen() else self.showFullScreen()

    def show_about(self) -> None:
        QMessageBox.about(
            self,
            "About NeuroFence",
            (
                "<b>NeuroFence v1.0</b><br><br>"
                "LLM Weight Poisoning &amp; Backdoor Scanner<br>"
                "Enterprise cybersecurity dashboard built with PyQt6."
            ),
        )
