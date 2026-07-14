"""System health overview card used by the NeuroFence dashboard."""

from __future__ import annotations

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout


class SystemStatusCard(QFrame):
    """Placeholder system metrics prepared for future live backend data."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("SystemStatusCard")
        self._status_labels: dict[str, QLabel] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(16)

        title = QLabel("Real-Time System Overview")
        title.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        title.setStyleSheet("color: #58A6FF;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(14)

        initial_values = [
            ("cpu", "CPU Status", "Normal · 24%"),
            ("ram", "RAM Status", "Normal · 46%"),
            ("gpu", "GPU Status", "Available"),
            ("scanner", "Scanner Status", "Ready"),
        ]

        for row, (key, title_text, value_text) in enumerate(initial_values):
            label = QLabel(title_text)
            label.setStyleSheet("color: #8B949E; font-size: 12px;")

            value = QLabel(value_text)
            value.setStyleSheet("color: #3FB950; font-size: 13px; font-weight: 600;")

            grid.addWidget(label, row, 0)
            grid.addWidget(value, row, 1)
            self._status_labels[key] = value

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        layout.addLayout(grid)
        layout.addStretch()

        self.setStyleSheet(
            """
            QFrame#SystemStatusCard {
                background: #161B22;
                border: 1px solid #30363D;
                border-radius: 15px;
            }
            """
        )

    def set_status(self, key: str, text: str, state: str = "normal") -> None:
        label = self._status_labels.get(key)
        if label is None:
            return
        colors = {
            "normal": "#3FB950",
            "scanning": "#58A6FF",
            "warning": "#F2CC60",
            "critical": "#F85149",
            "offline": "#8B949E",
        }
        color = colors.get(state.lower(), "#C9D1D9")
        label.setText(text)
        label.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: 600;")

    def set_scanner_status(self, text: str, state: str = "normal") -> None:
        self.set_status("scanner", text, state)
