"""Reusable recent scan summary panel for NeuroFence."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout


class RecentScanPanel(QFrame):
    """Displays the most recent model scan summary."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("RecentScanPanel")
        self._value_labels: dict[str, QLabel] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(16)

        title = QLabel("Recent Scan")
        title.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        title.setStyleSheet("color: #58A6FF;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(28)
        grid.setVerticalSpacing(14)

        fields = [
            ("last_scan", "Last Scan Time", "Not scanned yet"),
            ("model", "Last Model Loaded", "No model"),
            ("threat", "Threat Score", "0%"),
            ("duration", "Scan Duration", "--"),
            ("result", "Result", "READY"),
        ]

        for row, (key, label_text, initial_value) in enumerate(fields):
            label = QLabel(label_text)
            label.setStyleSheet("color: #8B949E; font-size: 12px;")

            value = QLabel(initial_value)
            value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            value.setStyleSheet("color: white; font-size: 13px; font-weight: 600;")
            value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            grid.addWidget(label, row, 0)
            grid.addWidget(value, row, 1)
            self._value_labels[key] = value

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        layout.addLayout(grid)
        layout.addStretch()

        self.setStyleSheet(
            """
            QFrame#RecentScanPanel {
                background: #161B22;
                border: 1px solid #30363D;
                border-radius: 15px;
            }
            """
        )

    def update_scan(
        self,
        *,
        scan_time: str,
        model_name: str,
        threat_score: int,
        duration_seconds: float,
        result: str,
    ) -> None:
        self._value_labels["last_scan"].setText(scan_time)
        self._value_labels["model"].setText(model_name)
        self._value_labels["threat"].setText(f"{threat_score}%")
        self._value_labels["duration"].setText(f"{duration_seconds:.1f} sec")
        self.set_result(result)

    def set_result(self, result: str) -> None:
        normalized = result.strip().upper()
        self._value_labels["result"].setText(normalized)
        color = {
            "SAFE": "#3FB950",
            "PROTECTED": "#3FB950",
            "WARNING": "#F2CC60",
            "CRITICAL": "#F85149",
            "SCANNING": "#58A6FF",
        }.get(normalized, "#C9D1D9")
        self._value_labels["result"].setStyleSheet(
            f"color: {color}; font-size: 13px; font-weight: 700;"
        )

    def reset(self) -> None:
        self._value_labels["last_scan"].setText("Not scanned yet")
        self._value_labels["model"].setText("No model")
        self._value_labels["threat"].setText("0%")
        self._value_labels["duration"].setText("--")
        self.set_result("READY")
