"""Structured, auto-scrolling security event console."""
from __future__ import annotations

from datetime import datetime
from html import escape

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget


class LogsWidget(QWidget):
    LEVEL_COLORS = {
        "INFO": "#60A5FA",
        "SUCCESS": "#34D399",
        "SAFE": "#2DD4BF",
        "WARNING": "#FBBF24",
        "ERROR": "#FB7185",
    }

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.entry_count = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        heading = QVBoxLayout()
        heading.setSpacing(2)
        title = QLabel("Security Event Stream")
        title.setObjectName("cardTitle")
        subtitle = QLabel("Timestamped scanner telemetry and detection output")
        subtitle.setObjectName("cardDescription")
        heading.addWidget(title)
        heading.addWidget(subtitle)

        self.counter = QLabel("0 EVENTS")
        self.counter.setObjectName("logCounter")
        clear_button = QPushButton("Clear")
        clear_button.setObjectName("secondaryButton")
        clear_button.clicked.connect(self.clear_logs)

        header.addLayout(heading, 1)
        header.addWidget(self.counter)
        header.addWidget(clear_button)

        self.logs = QTextEdit()
        self.logs.setObjectName("securityConsole")
        self.logs.setReadOnly(True)
        self.logs.setAcceptRichText(True)
        self.logs.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.logs.document().setMaximumBlockCount(1000)

        layout.addLayout(header)
        layout.addWidget(self.logs, 1)

        self.add_log("NeuroFence initialized", "INFO")
        self.add_log("Scanner services verified", "SUCCESS")
        self.add_log("Waiting for model upload", "INFO")

    def add_log(self, message: str, level: str = "INFO", timestamp: str | None = None) -> None:
        level = level.upper()
        timestamp = timestamp or datetime.now().strftime("%H:%M:%S")
        color = self.LEVEL_COLORS.get(level, "#CBD5E1")
        html = (
            f'<span style="color:#64748B;">{timestamp}</span>&nbsp;&nbsp;'
            f'<span style="color:{color}; font-weight:700;">{level:<7}</span>&nbsp;&nbsp;'
            f'<span style="color:#D7E2F0;">{escape(message)}</span>'
        )
        self.logs.append(html)
        self.logs.moveCursor(QTextCursor.MoveOperation.End)
        self.logs.ensureCursorVisible()
        self.entry_count += 1
        self.counter.setText(f"{self.entry_count} EVENTS")

    def clear_logs(self) -> None:
        self.logs.clear()
        self.entry_count = 0
        self.counter.setText("0 EVENTS")

    def append_log(self, level: str, message: str, timestamp: str | None = None) -> None:
        """Append one structured event using level-first data binding."""
        self.add_log(message, level, timestamp)
