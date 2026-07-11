from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(240)
        self.setObjectName("sidebar")

        layout = QVBoxLayout()

        layout.setContentsMargins(20, 25, 20, 25)

        layout.setSpacing(15)

        logo = QLabel("🛡 NeuroFence")

        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo.setObjectName("logo")

        layout.addWidget(logo)

        buttons = [
            "Dashboard",
            "Model Loader",
            "Security Scan",
            "Reports",
            "Settings"
        ]

        for text in buttons:

            btn = QPushButton(text)

            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            layout.addWidget(btn)

        layout.addStretch()

        self.setLayout(layout)