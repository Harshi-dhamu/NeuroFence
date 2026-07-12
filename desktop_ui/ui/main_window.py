from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)

from desktop_ui.widgets.progress_card import ProgressCard
from desktop_ui.widgets.activity_widget import ActivityWidget

from PyQt6.QtCore import Qt

from desktop_ui.widgets.sidebar import Sidebar
from desktop_ui.widgets.info_card import InfoCard
from desktop_ui.widgets.upload_card import UploadCard
from desktop_ui.widgets.scan_card import ScanCard
from desktop_ui.widgets.logs_widget import LogsWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NeuroFence")

        self.resize(1400, 850)

        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout()

        root_layout.setContentsMargins(0, 0, 0, 0)

        root_layout.setSpacing(0)

        central_widget.setLayout(root_layout)

        ###################################################
        # Sidebar
        ###################################################

        sidebar = Sidebar()

        root_layout.addWidget(sidebar)

        ###################################################
        # Right Side
        ###################################################

        right_widget = QWidget()

        right_layout = QVBoxLayout()

        right_layout.setContentsMargins(25, 20, 25, 20)

        right_layout.setSpacing(20)

        right_widget.setLayout(right_layout)

        root_layout.addWidget(right_widget)

        ###################################################
        # Header
        ###################################################

        title = QLabel("NeuroFence Dashboard")

        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            color:#58A6FF;
        """)

        subtitle = QLabel(
            "LLM Weight Poisoning & Backdoor Scanner"
        )

        subtitle.setStyleSheet("""
            color:#8B949E;
            font-size:13px;
        """)

        right_layout.addWidget(title)

        right_layout.addWidget(subtitle)

        ###################################################
        # Statistics Cards
        ###################################################

        stats_layout = QGridLayout()

        stats_layout.setHorizontalSpacing(20)

        stats_layout.setVerticalSpacing(20)

        card1 = InfoCard(
            "Models Loaded",
            "0"
        )

        card2 = InfoCard(
            "Threat Score",
            "0%"
        )

        card3 = InfoCard(
            "Scan Status",
            "Ready"
        )

        stats_layout.addWidget(card1, 0, 0)

        stats_layout.addWidget(card2, 0, 1)

        stats_layout.addWidget(card3, 0, 2)

        right_layout.addLayout(stats_layout)

        ###################################################
        # Upload + Scan
        ###################################################

        middle_layout = QHBoxLayout()

        middle_layout.setSpacing(20)

        self.upload_card = UploadCard()

        self.scan_card = ScanCard()

        middle_layout.addWidget(self.upload_card)

        middle_layout.addWidget(self.scan_card)

        right_layout.addLayout(middle_layout)
        
        bottom_layout = QHBoxLayout()

        bottom_layout.setSpacing(20)

        self.activity = ActivityWidget()

        self.progress_card = ProgressCard()

        bottom_layout.addWidget(self.activity)

        bottom_layout.addWidget(self.progress_card)

        right_layout.addLayout(bottom_layout)
        
        ###################################################
        # Live Logs
        ###################################################

        self.logs_widget = LogsWidget()

        right_layout.addWidget(self.logs_widget)

        ###################################################
        # Stretch
        ###################################################

        right_layout.addStretch()

        ###################################################
        # Status Bar
        ###################################################

        self.statusBar().showMessage("✔ Ready | NeuroFence Desktop v1.0 | AI Security")

        ###################################################
        # Menu Bar
        ###################################################

        file_menu = self.menuBar().addMenu("File")

        help_menu = self.menuBar().addMenu("Help")

        exit_action = file_menu.addAction("Exit")

        about_action = help_menu.addAction("About")

        exit_action.triggered.connect(self.close)

        about_action.triggered.connect(self.show_about)

        ###################################################
        # Connect Buttons
        ###################################################

        self.scan_card.scan_button.clicked.connect(self.start_scan)

    ###################################################
    # Scan Demo
    ###################################################

    def start_scan(self):

        self.progress_card.progress.setValue(0)

        self.activity.add_activity("Security scan started")

        self.logs_widget.add_log("Starting scan...")

        self.progress_card.progress.setValue(20)

        self.activity.add_activity("Checking model")

        self.logs_widget.add_log("Checking model...")

        self.progress_card.progress.setValue(40)

        self.activity.add_activity("Analyzing weights")

        self.logs_widget.add_log("Analyzing weights...")

        self.progress_card.progress.setValue(60)

        self.activity.add_activity("Searching hidden neurons")

        self.logs_widget.add_log("Searching dormant neurons...")

        self.progress_card.progress.setValue(80)

        self.activity.add_activity("Running adversarial prompts")

        self.logs_widget.add_log("Running prompts...")

        self.progress_card.progress.setValue(100)

        self.activity.add_activity("Scan completed")

        self.logs_widget.add_log("Scan Complete")

        self.statusBar().showMessage("Scan Finished")

        self.scan_card.status.setText("Status : Scan Complete")

    ###################################################
    # About Dialog
    ###################################################

    def show_about(self):

        self.logs_widget.add_log("")

        self.logs_widget.add_log("NeuroFence v1.0")

        self.logs_widget.add_log(
            "AI Security | LLM Weight Poisoning Scanner"
        )

        self.logs_widget.add_log(
            "Developed as Internship Project"
        )