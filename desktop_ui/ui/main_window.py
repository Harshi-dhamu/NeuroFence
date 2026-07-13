"""Main application window for the NeuroFence desktop UI.

This module is intentionally compatible with the existing widgets in the
project ZIP.  It adds a scrollable, responsive dashboard and performs the demo
scan asynchronously so the interface remains responsive.
"""

from __future__ import annotations

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from desktop_ui.components.circular_gauge import CircularGauge
from desktop_ui.components.system_info import SystemInfo
from desktop_ui.components.top_bar import TopBar
from desktop_ui.widgets.activity_widget import ActivityWidget
from desktop_ui.widgets.info_card import InfoCard
from desktop_ui.widgets.logs_widget import LogsWidget
from desktop_ui.widgets.progress_card import ProgressCard
from desktop_ui.widgets.scan_card import ScanCard
from desktop_ui.widgets.sidebar import Sidebar
from desktop_ui.widgets.upload_card import UploadCard


class MainWindow(QMainWindow):
    """Responsive main window for the NeuroFence security dashboard."""

    COMPACT_WIDTH = 1050

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("NeuroFence Enterprise AI Security Platform")
        self.resize(1500, 900)
        self.setMinimumSize(820, 600)

        self._compact_mode: bool | None = None
        self._scan_step_index = 0
        self._scan_steps: list[tuple[int, int, str, str]] = []

        self.scan_timer = QTimer(self)
        self.scan_timer.setInterval(550)
        self.scan_timer.timeout.connect(self._run_next_scan_step)

        self.setup_ui()
        self.setup_menu()
        self.connect_signals()

        self.statusBar().showMessage(
            "✔ Ready | NeuroFence Enterprise v1.0 | AI Security Platform"
        )

        # Apply the correct layout after Qt has completed the first geometry pass.
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
        self.sidebar.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )
        self._ensure_sidebar_help_action()
        root_layout.addWidget(self.sidebar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        root_layout.addWidget(self.scroll_area, 1)

        self.dashboard_widget = QWidget()
        self.dashboard_widget.setObjectName("dashboardWidget")
        self.scroll_area.setWidget(self.dashboard_widget)

        self.dashboard_layout = QVBoxLayout(self.dashboard_widget)
        self.dashboard_layout.setContentsMargins(28, 28, 28, 28)
        self.dashboard_layout.setSpacing(26)

        self.top_bar = TopBar()
        self.top_bar.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.dashboard_layout.addWidget(self.top_bar)

        self._build_statistics_section()
        self._build_action_section()
        self._build_analysis_section()
        self._build_activity_section()

        self.logs_widget = LogsWidget()
        self.logs_widget.setMinimumHeight(180)
        self.logs_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self.dashboard_layout.addWidget(self.logs_widget, 1)

    def _build_statistics_section(self) -> None:
        self.stats_container = QWidget()
        self.stats_layout = QGridLayout(self.stats_container)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_layout.setHorizontalSpacing(24)
        self.stats_layout.setVerticalSpacing(24)

        self.card_models = InfoCard("Models Loaded", "0")
        self.card_threat = InfoCard("Threat Score", "0%")
        self.card_status = InfoCard("System Status", "Ready")
        self.stat_cards = [
            self.card_models,
            self.card_threat,
            self.card_status,
        ]

        for card in self.stat_cards:
            card.setObjectName("card")
            card.setMinimumHeight(115)
            card.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred,
            )

        self.dashboard_layout.addWidget(self.stats_container)

    def _build_action_section(self) -> None:
        self.action_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.action_splitter.setChildrenCollapsible(False)
        self.action_splitter.setHandleWidth(8)

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
        self.analysis_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.analysis_splitter.setChildrenCollapsible(False)
        self.analysis_splitter.setHandleWidth(8)

        self.gauge = CircularGauge()
        self.gauge.setMinimumSize(220, 220)
        self.gauge.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.system_info = SystemInfo()
        self.system_info.setMinimumSize(320, 220)
        self.system_info.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.analysis_splitter.addWidget(self.gauge)
        self.analysis_splitter.addWidget(self.system_info)
        self.analysis_splitter.setStretchFactor(0, 2)
        self.analysis_splitter.setStretchFactor(1, 3)
        self.analysis_splitter.setSizes([400, 600])

        self.dashboard_layout.addWidget(self.analysis_splitter)

    def _build_activity_section(self) -> None:
        self.activity_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.activity_splitter.setChildrenCollapsible(False)
        self.activity_splitter.setHandleWidth(8)

        self.activity = ActivityWidget()
        self.progress_card = ProgressCard()

        self.activity.setMinimumHeight(165)
        self.progress_card.setMinimumHeight(165)
        self.progress_card.setObjectName("card")

        self.activity_splitter.addWidget(self.activity)
        self.activity_splitter.addWidget(self.progress_card)
        self.activity_splitter.setStretchFactor(0, 2)
        self.activity_splitter.setStretchFactor(1, 1)
        self.activity_splitter.setSizes([650, 350])

        self.dashboard_layout.addWidget(self.activity_splitter)

    def _ensure_sidebar_help_action(self) -> None:
        """Add the Help navigation item required by the dashboard design."""
        sidebar_layout = self.sidebar.layout()
        if sidebar_layout is None:
            return

        existing_buttons = self.sidebar.findChildren(QPushButton)
        if any(button.text().strip().lower() == "help" for button in existing_buttons):
            return

        help_button = QPushButton("Help")
        help_button.setCursor(Qt.CursorShape.PointingHandCursor)
        help_button.clicked.connect(self.show_about)
        # Sidebar ends with a stretch, so insert Help immediately before it.
        sidebar_layout.insertWidget(max(0, sidebar_layout.count() - 1), help_button)

    def setup_menu(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        tools_menu = self.menuBar().addMenu("Tools")
        help_menu = self.menuBar().addMenu("Help")

        exit_action = file_menu.addAction("Exit")
        reset_action = tools_menu.addAction("Reset Dashboard")
        fullscreen_action = tools_menu.addAction("Toggle Full Screen")
        about_action = help_menu.addAction("About NeuroFence")

        exit_action.triggered.connect(self.close)
        reset_action.triggered.connect(self.reset_dashboard)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        about_action.triggered.connect(self.show_about)

    def connect_signals(self) -> None:
        self.scan_card.scan_button.clicked.connect(self.start_scan)
        self.upload_card.button.clicked.connect(self._model_selection_changed)

    # ------------------------------------------------------------------
    # Responsive behaviour
    # ------------------------------------------------------------------

    def resizeEvent(self, event) -> None:  # noqa: N802 (Qt API name)
        super().resizeEvent(event)
        self._update_responsive_layout()

    def _update_responsive_layout(self) -> None:
        compact = self.width() < self.COMPACT_WIDTH
        if compact == self._compact_mode:
            return

        self._compact_mode = compact

        sidebar_width = 175 if compact else 240
        self.sidebar.setFixedWidth(sidebar_width)

        orientation = (
            Qt.Orientation.Vertical if compact else Qt.Orientation.Horizontal
        )
        for splitter in (
            self.action_splitter,
            self.analysis_splitter,
            self.activity_splitter,
        ):
            splitter.setOrientation(orientation)

        self._arrange_stat_cards(compact)

        if compact:
            self.action_splitter.setSizes([210, 210])
            self.analysis_splitter.setSizes([245, 245])
            self.activity_splitter.setSizes([175, 175])
        else:
            self.action_splitter.setSizes([600, 400])
            self.analysis_splitter.setSizes([400, 600])
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
    # Dashboard state helpers
    # ------------------------------------------------------------------

    def _add_log(self, message: str, level: str = "INFO") -> None:
        """Append a timestamped, enterprise-style log entry."""
        timestamp = __import__("datetime").datetime.now().strftime("%H:%M:%S")
        self.logs_widget.add_log(f"[{timestamp}] [{level}] {message}")

    @staticmethod
    def _set_info_card_value(card: InfoCard, value: str) -> None:
        """Update an existing InfoCard without requiring widget API changes."""
        value_label = card.findChild(QLabel, "cardValue")
        if value_label is not None:
            value_label.setText(value)

    def _model_selection_changed(self) -> None:
        # QFileDialog runs before this slot because UploadCard connected first.
        if self.upload_card.model_path:
            self._set_info_card_value(self.card_models, "1")
            self.activity.add_activity("Model folder selected")
            self._add_log(f"Selected model: {self.upload_card.model_path}")
            self.statusBar().showMessage("Model folder loaded and ready to scan")

    def reset_dashboard(self) -> None:
        self.scan_timer.stop()
        self._scan_step_index = 0
        self.scan_card.scan_button.setEnabled(True)
        self.scan_card.status.setText("Status : Ready")
        self.progress_card.progress.setValue(0)
        self.gauge.setValue(5)

        self.activity.list.clear()
        self.activity.add_activity("NeuroFence initialized")
        self.activity.add_activity("Waiting for model")

        self.logs_widget.logs.clear()
        self._add_log("NeuroFence initialized")
        self._add_log("Waiting for model upload")
        self._add_log("System ready", "SUCCESS")

        self._set_info_card_value(
            self.card_models,
            "1" if self.upload_card.model_path else "0",
        )
        self._set_info_card_value(self.card_threat, "0%")
        self._set_info_card_value(self.card_status, "Ready")
        self.statusBar().showMessage("✔ Dashboard reset | Ready")

    # ------------------------------------------------------------------
    # Scan demo
    # ------------------------------------------------------------------

    def start_scan(self) -> None:
        if self.scan_timer.isActive():
            return

        if not self.upload_card.model_path:
            self._add_log(
                "No model folder selected; running demonstration scan",
                "WARNING",
            )

        self.logs_widget.logs.clear()
        self.activity.list.clear()
        self.progress_card.progress.setValue(0)
        self.gauge.setValue(5)
        self.scan_card.status.setText("Status : Scanning")
        self.scan_card.scan_button.setEnabled(False)

        self._set_info_card_value(self.card_threat, "Scanning...")
        self._set_info_card_value(self.card_status, "Scanning")
        if self.upload_card.model_path:
            self._set_info_card_value(self.card_models, "1")

        self.statusBar().showMessage("Initializing security scan...")

        self._scan_steps = [
            (10, 10, "Security scan started", "Initializing NeuroFence..."),
            (25, 18, "Checking model structure", "Checking model architecture..."),
            (40, 30, "Loading model weights", "Loading model weights..."),
            (
                60,
                45,
                "Searching dormant neurons",
                "Scanning hidden neuron activations...",
            ),
            (
                80,
                65,
                "Running adversarial prompts",
                "Executing prompt fuzzing...",
            ),
            (
                95,
                18,
                "Generating security report",
                "Generating analysis report...",
            ),
        ]
        self._scan_step_index = 0
        self.scan_timer.start()

    def _run_next_scan_step(self) -> None:
        if self._scan_step_index >= len(self._scan_steps):
            self.scan_timer.stop()
            self._finish_scan()
            return

        progress, threat, activity_text, log_text = self._scan_steps[
            self._scan_step_index
        ]
        self.progress_card.progress.setValue(progress)
        self.gauge.setValue(threat)
        self.activity.add_activity(activity_text)
        self._add_log(log_text)
        self.statusBar().showMessage(activity_text)
        self._scan_step_index += 1

    def _finish_scan(self) -> None:
        self.activity.add_activity("Scan completed successfully")
        self._add_log("No weight poisoning detected", "SAFE")
        self._add_log("No dormant backdoor trigger found", "SAFE")
        self._add_log("Threat score: 18%", "INFO")
        self._add_log("Model status: SAFE", "SUCCESS")

        self.progress_card.progress.setValue(100)
        self.gauge.setValue(18)
        self.scan_card.status.setText("Status : Protected")
        self.scan_card.scan_button.setEnabled(True)

        self._set_info_card_value(
            self.card_models,
            "1" if self.upload_card.model_path else "Demo",
        )
        self._set_info_card_value(self.card_threat, "18%")
        self._set_info_card_value(self.card_status, "Protected")
        self.statusBar().showMessage("✔ Scan completed successfully")

    # ------------------------------------------------------------------
    # Window actions
    # ------------------------------------------------------------------

    def toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def show_about(self) -> None:
        QMessageBox.about(
            self,
            "About NeuroFence",
            (
                "<b>NeuroFence v1.0</b><br><br>"
                "Enterprise AI Security Platform<br>"
                "LLM Weight Poisoning &amp; Backdoor Scanner<br><br>"
                "Developed using PyQt6"
            ),
        )
