"""Professional dashboard header for NeuroFence."""
from __future__ import annotations

from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class TopBar(QFrame):
    STATUS_COLORS = {
        "Protected": "#2DD4BF",
        "Scanning": "#60A5FA",
        "Warning": "#FBBF24",
        "Critical": "#FB7185",
        "Ready": "#94A3B8",
    }

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("TopBar")
        self.setMinimumHeight(126)
        self._build_ui()
        self._start_clock()

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(26, 20, 26, 20)
        layout.setSpacing(26)

        identity = QVBoxLayout()
        identity.setSpacing(4)
        eyebrow = QLabel("NEUROFENCE SECURITY OPERATIONS")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("LLM Integrity Dashboard")
        title.setObjectName("heroTitle")
        subtitle = QLabel("Weight poisoning, dormant backdoor and adversarial trigger analysis")
        subtitle.setObjectName("heroSubtitle")
        subtitle.setWordWrap(True)
        identity.addWidget(eyebrow)
        identity.addWidget(title)
        identity.addWidget(subtitle)
        layout.addLayout(identity, 3)

        clock_box = QFrame()
        clock_box.setObjectName("headerMiniCard")
        clock_layout = QVBoxLayout(clock_box)
        clock_layout.setContentsMargins(16, 12, 16, 12)
        clock_layout.setSpacing(2)
        clock_caption = QLabel("LOCAL SECURITY TIME")
        clock_caption.setObjectName("miniCaption")
        self.time_label = QLabel()
        self.time_label.setObjectName("clockValue")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label = QLabel()
        self.date_label.setObjectName("miniCaption")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clock_layout.addWidget(clock_caption)
        clock_layout.addWidget(self.time_label)
        clock_layout.addWidget(self.date_label)
        layout.addWidget(clock_box, 1)

        status_box = QFrame()
        status_box.setObjectName("headerMiniCard")
        status_layout = QVBoxLayout(status_box)
        status_layout.setContentsMargins(16, 12, 16, 12)
        status_layout.setSpacing(4)
        status_caption = QLabel("OVERALL SYSTEM STATUS")
        status_caption.setObjectName("miniCaption")
        status_caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label = QLabel("●  Protected")
        self.status_label.setObjectName("headerStatus")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_hint = QLabel("All monitoring services operational")
        status_hint.setObjectName("miniCaption")
        status_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(status_caption)
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(status_hint)
        layout.addWidget(status_box, 1)

    def _start_clock(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

    def update_clock(self) -> None:
        now = datetime.now()
        self.time_label.setText(now.strftime("%I:%M:%S %p"))
        self.date_label.setText(now.strftime("%a, %d %b %Y"))

    def set_system_status(self, status: str) -> None:
        normalized = status.strip().title()
        color = self.STATUS_COLORS.get(normalized, "#CBD5E1")
        self.status_label.setText(f"●  {normalized}")
        self.status_label.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: 700;")
