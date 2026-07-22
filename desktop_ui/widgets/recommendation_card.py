from __future__ import annotations
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class RecommendationCard(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setObjectName("RecommendationCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(10)

        title = QLabel("Recommendations")
        title.setObjectName("sectionTitle")

        self.text = QLabel(
            "Complete a scan to generate security recommendations."
        )
        self.text.setObjectName("recommendationText")
        self.text.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(self.text)

    def set_recommendations(self, recommendations):
        if isinstance(recommendations, list):
            recommendations = "\n".join(
                f"• {item}" for item in recommendations
            )

        self.text.setText(
            recommendations or "No recommendation available."
        )