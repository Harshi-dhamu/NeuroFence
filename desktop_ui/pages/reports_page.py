"""Reports dashboard page for NeuroFence."""

from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QScrollArea, QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from desktop_ui.components.report_summary_card import ReportSummaryCard
from desktop_ui.components.threat_statistics import ThreatStatistics
from desktop_ui.widgets.info_card import InfoCard


class ReportsPage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ReportsPage")
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._build_ui()

    def _build_ui(self):
        content = QWidget()
        content.setObjectName("pageContent")
        self.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 28, 28, 32)
        layout.setSpacing(26)

        eyebrow = QLabel("SECURITY INTELLIGENCE")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Reports Dashboard")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Review scan outcomes, model risk distribution and the latest security assessment.")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        stats = QGridLayout()
        stats.setSpacing(18)
        self.total_models = InfoCard("Models Scanned", "24", "Total completed inspections")
        self.safe_models = InfoCard("Safe Models", "21", "Models cleared by NeuroFence")
        self.suspicious_models = InfoCard("Suspicious", "3", "Models requiring investigation")
        self.average_threat = InfoCard("Average Threat", "14%", "Average recorded risk score")
        self.last_scan = InfoCard("Last Scan", "TinyLlama", "Most recently inspected model")
        self.last_duration = InfoCard("Duration", "4.1 sec", "Latest scan completion time")
        self.summary_cards = [self.total_models, self.safe_models, self.suspicious_models, self.average_threat, self.last_scan, self.last_duration]
        for index, card in enumerate(self.summary_cards):
            card.setObjectName("card")
            card.setMinimumHeight(112)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            stats.addWidget(card, index // 3, index % 3)
        layout.addLayout(stats)

        details = QGridLayout()
        details.setSpacing(22)
        self.report_summary = ReportSummaryCard()
        self.threat_statistics = ThreatStatistics()
        details.addWidget(self.report_summary, 0, 0, 1, 3)
        details.addWidget(self.threat_statistics, 0, 3, 1, 2)
        details.setColumnStretch(0, 1)
        details.setColumnStretch(1, 1)
        details.setColumnStretch(2, 1)
        details.setColumnStretch(3, 1)
        details.setColumnStretch(4, 1)
        layout.addLayout(details)
        layout.addStretch()

    def update_latest_report(self, model_name, result, threat_score, duration, scan_time, recommendation):
        self.report_summary.update_report(model_name, result, threat_score, scan_time, recommendation)
        self.last_scan.set_value(model_name)
        self.last_duration.set_value(f"{duration:.1f} sec")
