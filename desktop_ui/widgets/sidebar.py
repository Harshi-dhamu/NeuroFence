from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QButtonGroup, QFrame, QLabel, QPushButton, QVBoxLayout


class Sidebar(QFrame):
    """Enterprise navigation rail. Existing code can still resize it."""

    def __init__(self):
        super().__init__()
        self.setFixedWidth(240)
        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 24, 18, 22)
        layout.setSpacing(8)

        brand = QLabel("NF")
        brand.setObjectName("brandMark")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.setFixedSize(44, 44)

        logo = QLabel("NeuroFence")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        brand_row = QVBoxLayout()
        brand_row.setSpacing(7)
        brand_row.addWidget(brand, 0, Qt.AlignmentFlag.AlignLeft)
        brand_row.addWidget(logo)
        layout.addLayout(brand_row)

        descriptor = QLabel("AI MODEL SECURITY")
        descriptor.setObjectName("sidebarCaption")
        layout.addWidget(descriptor)
        layout.addSpacing(18)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        items = [
            ("▦", "Dashboard"),
            ("⬡", "Model Loader"),
            ("⌁", "Security Scan"),
            ("▤", "Reports"),
            ("⚙", "Settings"),
        ]
        self.buttons = []
        for index, (icon, text) in enumerate(items):
            button = QPushButton(f"{icon}   {text}")
            button.setObjectName("navButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            if index == 0:
                button.setChecked(True)
            self.button_group.addButton(button)
            self.buttons.append(button)
            layout.addWidget(button)

        layout.addStretch()

        footer = QLabel("●  Protection online\nNeuroFence v1.0")
        footer.setObjectName("sidebarFooter")
        layout.addWidget(footer)
