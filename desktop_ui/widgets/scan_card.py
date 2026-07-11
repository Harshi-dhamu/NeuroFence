from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)


class ScanCard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("card")

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("🛡 Security Scan")
        title.setObjectName("cardTitle")

        description = QLabel(
            "Run NeuroFence to detect poisoned weights and hidden backdoors."
        )

        description.setWordWrap(True)
        description.setObjectName("cardDescription")

        self.status = QLabel("Status : Ready")
        self.status.setObjectName("statusReady")

        self.scan_button = QPushButton("▶ RUN SECURITY SCAN")
        self.scan_button.setObjectName("scanButton")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.status)
        layout.addWidget(self.scan_button)
        layout.addStretch()

        self.setLayout(layout)