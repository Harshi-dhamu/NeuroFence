from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
)

from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NeuroFence")

        self.setMinimumSize(1200, 700)

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout()

        central.setLayout(layout)

        title = QLabel("NeuroFence")

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            font-size:34px;
            font-weight:bold;
        """)

        subtitle = QLabel(
            "LLM Weight Poisoning & Backdoor Scanner"
        )

        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle.setStyleSheet("""
            font-size:16px;
            color:#AAAAAA;
        """)

        layout.addStretch()

        layout.addWidget(title)

        layout.addWidget(subtitle)

        layout.addStretch()

        self.statusBar().showMessage("Ready")

        self.menuBar().addMenu("File")

        self.menuBar().addMenu("Help")