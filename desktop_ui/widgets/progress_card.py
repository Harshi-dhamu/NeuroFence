from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget


class ProgressCard(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 20)
        layout.setSpacing(14)

        title = QLabel("Scan Progress")
        title.setObjectName("cardTitle")
        subtitle = QLabel("Multi-stage model integrity inspection")
        subtitle.setObjectName("cardDescription")

        self.stage_label = QLabel("Ready to scan")
        self.stage_label.setObjectName("progressStage")

        self.progress = QProgressBar()
        self.progress.setObjectName("securityProgress")
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setFormat("%p%")
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hint = QLabel("Scanner remains responsive during analysis")
        hint.setObjectName("metricSubtitle")
        hint.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(self.stage_label)
        layout.addWidget(self.progress)
        layout.addWidget(hint)

    def set_stage(self, text: str) -> None:
        self.stage_label.setText(text)
