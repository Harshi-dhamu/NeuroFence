"""Reusable glass-style summary card for the latest NeuroFence report."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout


class ReportSummaryCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ReportSummaryCard")
        self.setMinimumHeight(285)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)

        eyebrow = QLabel("LATEST SECURITY ASSESSMENT")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Report Summary")
        title.setObjectName("sectionTitle")
        layout.addWidget(eyebrow)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(28)
        grid.setVerticalSpacing(15)
        self.model_value = self._metric(grid, 0, 0, "MODEL", "Demo Model")
        self.result_value = self._metric(grid, 0, 1, "RESULT", "READY", "safeValue")
        self.threat_value = self._metric(grid, 1, 0, "THREAT SCORE", "0%")
        self.time_value = self._metric(grid, 1, 1, "SCAN TIME", "—")
        layout.addLayout(grid)

        recommendation_title = QLabel("RECOMMENDATION")
        recommendation_title.setObjectName("miniCaption")
        self.recommendation_value = QLabel("Run a security scan to generate a recommendation.")
        self.recommendation_value.setObjectName("recommendationText")
        self.recommendation_value.setWordWrap(True)
        self.recommendation_value.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(recommendation_title)
        layout.addWidget(self.recommendation_value)
        layout.addStretch()

    @staticmethod
    def _metric(grid, row, column, title, value, object_name="reportMetricValue"):
        holder = QFrame()
        holder.setObjectName("glassInnerCard")
        box = QVBoxLayout(holder)
        box.setContentsMargins(14, 12, 14, 12)
        box.setSpacing(4)
        label = QLabel(title)
        label.setObjectName("miniCaption")
        value_label = QLabel(value)
        value_label.setObjectName(object_name)
        box.addWidget(label)
        box.addWidget(value_label)
        grid.addWidget(holder, row, column)
        return value_label

    def update_report(self, model_name, result, threat_score, scan_time, recommendation):
        self.model_value.setText(str(model_name))
        self.result_value.setText(str(result))
        self.threat_value.setText(f"{int(threat_score)}%")
        self.time_value.setText(str(scan_time))
        self.recommendation_value.setText(str(recommendation))
        self.result_value.setProperty("state", str(result).lower())
        self.result_value.style().unpolish(self.result_value)
        self.result_value.style().polish(self.result_value)
