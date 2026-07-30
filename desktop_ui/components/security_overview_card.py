from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QGridLayout,
    QVBoxLayout,
)


class SecurityOverviewCard(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("SecurityOverviewCard")

        layout = QVBoxLayout(self)

        title = QLabel("Security Overview")
        title.setObjectName("sectionTitle")

        layout.addWidget(title)

        grid = QGridLayout()

        self.total_scans = QLabel("0")
        self.average_score = QLabel("0%")
        self.high_risk = QLabel("0")
        self.models_analyzed = QLabel("0")

        cards = [
            ("Total Scans", self.total_scans),
            ("Average Threat Score", self.average_score),
            ("High Risk Models", self.high_risk),
            ("Models Analyzed", self.models_analyzed),
        ]

        for i, (label_text, value_label) in enumerate(cards):

            card = QFrame()
            card.setObjectName("glassInnerCard")

            card_layout = QVBoxLayout(card)

            label = QLabel(label_text)
            label.setObjectName("metricTitle")

            value_label.setObjectName("metricValue")

            card_layout.addWidget(label)
            card_layout.addWidget(value_label)

            grid.addWidget(card, i // 2, i % 2)

        layout.addLayout(grid)

    def update_metrics(
        self,
        total_scans,
        average_score,
        high_risk,
        models_analyzed,
    ):
        self.total_scans.setText(str(total_scans))
        self.average_score.setText(f"{average_score}%")
        self.high_risk.setText(str(high_risk))
        self.models_analyzed.setText(str(models_analyzed))