"""Animated enterprise navigation sidebar for NeuroFence."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QButtonGroup, QFrame, QLabel, QPushButton, QVBoxLayout


class Sidebar(QFrame):
    page_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setObjectName("sidebar")
        self.buttons_by_page = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 24, 18, 22)
        layout.setSpacing(8)

        brand = QLabel("NF")
        brand.setObjectName("brandMark")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.setFixedSize(44, 44)
        logo = QLabel("NeuroFence")
        logo.setObjectName("logo")
        descriptor = QLabel("AI MODEL SECURITY")
        descriptor.setObjectName("sidebarCaption")
        layout.addWidget(brand, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(logo)
        layout.addWidget(descriptor)
        layout.addSpacing(18)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        items = [
            ("dashboard", "▦", "Dashboard"),
            ("models", "⬡", "Models"),
            ("scan", "⌁", "Scan"),
            ("reports", "▤", "Reports"),
            ("history", "◷", "History"),
            ("settings", "⚙", "Settings"),
            ("help", "?", "Help"),
        ]
        for index, (page, icon, text) in enumerate(items):
            button = QPushButton(f"{icon}   {text}")
            button.setObjectName("navButton")
            button.setProperty("page", page)
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setChecked(index == 0)
            button.clicked.connect(lambda checked=False, name=page: self.page_requested.emit(name))
            self.button_group.addButton(button)
            self.buttons_by_page[page] = button
            layout.addWidget(button)

        layout.addStretch()
        footer = QLabel("●  Protection online\nNeuroFence v1.0")
        footer.setObjectName("sidebarFooter")
        layout.addWidget(footer)

    def select_page(self, page_name):
        button = self.buttons_by_page.get(page_name)
        if button is not None:
            button.setChecked(True)
