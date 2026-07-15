"""Threat distribution widget prepared for the detection backend."""

from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout


class ThreatStatistics(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ThreatStatistics")
        self.values = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)
        eyebrow = QLabel("MODEL RISK DISTRIBUTION")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Threat Statistics")
        title.setObjectName("sectionTitle")
        layout.addWidget(eyebrow)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(14)
        items = [
            ("critical", "Critical Threats", 0, "criticalStat"),
            ("medium", "Medium Threats", 2, "mediumStat"),
            ("low", "Low Threats", 5, "lowStat"),
            ("safe", "Safe Models", 17, "safeStat"),
        ]
        for index, (key, title_text, value, object_name) in enumerate(items):
            card = QFrame()
            card.setObjectName("glassInnerCard")
            box = QVBoxLayout(card)
            box.setContentsMargins(16, 14, 16, 14)
            title = QLabel(title_text)
            title.setObjectName("metricTitle")
            number = QLabel(str(value))
            number.setObjectName(object_name)
            box.addWidget(title)
            box.addWidget(number)
            grid.addWidget(card, index // 2, index % 2)
            self.values[key] = number
        layout.addLayout(grid)
        layout.addStretch()

    def set_statistics(self, *, critical=None, medium=None, low=None, safe=None):
        for key, value in {"critical": critical, "medium": medium, "low": low, "safe": safe}.items():
            if value is not None:
                self.values[key].setText(str(value))
