from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class InfoCard(QFrame):
    """Compact security KPI card with a stable Day 5/Day 6 API."""

    ICONS = {
        "models": "◫",
        "threat": "◎",
        "status": "●",
    }

    def __init__(self, title: str, value: str, subtitle: str = "Live dashboard metric"):
        super().__init__()
        self.setObjectName("card")
        self.setProperty("class", "metricCard")

        root = QHBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(16)

        key = "models" if "model" in title.lower() else "threat" if "threat" in title.lower() else "status"
        self.icon_label = QLabel(self.ICONS[key])
        self.icon_label.setObjectName("metricIcon")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFixedSize(46, 46)

        content = QVBoxLayout()
        content.setSpacing(3)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("metricTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("metricSubtitle")
        self.subtitle_label.setWordWrap(True)

        content.addWidget(self.title_label)
        content.addWidget(self.value_label)
        content.addWidget(self.subtitle_label)

        root.addWidget(self.icon_label)
        root.addLayout(content, 1)

    def set_value(self, value: str) -> None:
        self.value_label.setText(str(value))

    def set_title(self, title: str) -> None:
        self.title_label.setText(title)

    def set_subtitle(self, subtitle: str) -> None:
        self.subtitle_label.setText(subtitle)

    def set_icon(self, icon: str) -> None:
        self.icon_label.setText(icon)
