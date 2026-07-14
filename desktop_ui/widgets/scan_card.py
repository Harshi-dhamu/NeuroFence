from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class ScanCard(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(12)

        eyebrow = QLabel("SECURITY OPERATION")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Run Integrity Scan")
        title.setObjectName("cardTitle")
        description = QLabel("Inspect weight tensors, dormant neurons and adversarial trigger behaviour.")
        description.setWordWrap(True)
        description.setObjectName("cardDescription")

        self.status = QLabel("●  Ready for analysis")
        self.status.setObjectName("statusReady")

        self.scan_button = QPushButton("Run security scan")
        self.scan_button.setObjectName("scanButton")
        self.scan_button.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
        layout.addWidget(self.status)
        layout.addWidget(self.scan_button)
