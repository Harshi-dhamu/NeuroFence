from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class TopBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("TopBar")
        self.setFixedHeight(90)

        self.setup_ui()
        self.start_clock()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        # Left section
        left_layout = QVBoxLayout()

        title = QLabel("NeuroFence")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #58A6FF;")

        subtitle = QLabel("Enterprise AI Security Platform")
        subtitle.setStyleSheet(
            "color: #8B949E; font-size: 12px;"
        )

        left_layout.addWidget(title)
        left_layout.addWidget(subtitle)

        layout.addLayout(left_layout)
        layout.addStretch()

        # Centre clock section
        centre_layout = QVBoxLayout()

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: white;"
        )

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet(
            "color: #8B949E; font-size: 11px;"
        )

        centre_layout.addWidget(self.time_label)
        centre_layout.addWidget(self.date_label)

        layout.addLayout(centre_layout)
        layout.addStretch()

        # Right section
        right_layout = QVBoxLayout()

        user_label = QLabel("Administrator")
        user_label.setStyleSheet(
            "color: white; font-size: 14px; font-weight: bold;"
        )

        connection_label = QLabel("● Connected")
        connection_label.setStyleSheet(
            "color: #3FB950; font-size: 12px;"
        )

        right_layout.addWidget(user_label)
        right_layout.addWidget(connection_label)

        layout.addLayout(right_layout)

        self.setStyleSheet(
            """
            QFrame#TopBar {
                background: #161B22;
                border: 1px solid #30363D;
                border-radius: 12px;
            }
            """
        )

    def start_clock(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now = datetime.now()

        self.time_label.setText(now.strftime("%H:%M:%S"))
        self.date_label.setText(now.strftime("%A, %d %B %Y"))