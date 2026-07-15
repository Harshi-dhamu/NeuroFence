"""Searchable scan history page for NeuroFence."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from desktop_ui.widgets.history_table import HistoryTable


class HistoryPage(QScrollArea):
    export_requested = pyqtSignal()
    filter_requested = pyqtSignal()
    search_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HistoryPage")
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
        layout.setSpacing(24)

        eyebrow = QLabel("AUDIT TRAIL")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Scan History")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Search completed model inspections and prepare records for export.")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        toolbar = QFrame()
        toolbar.setObjectName("glassToolbar")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(16, 14, 16, 14)
        toolbar_layout.setSpacing(12)
        self.search_box = QLineEdit()
        self.search_box.setObjectName("historySearch")
        self.search_box.setPlaceholderText("Search by scan ID, model, date, score or result…")
        self.filter_button = QPushButton("Filter")
        self.filter_button.setObjectName("secondaryButton")
        self.export_button = QPushButton("Export")
        self.export_button.setObjectName("primaryButton")
        toolbar_layout.addWidget(self.search_box, 1)
        toolbar_layout.addWidget(self.filter_button)
        toolbar_layout.addWidget(self.export_button)
        layout.addWidget(toolbar)

        table_frame = QFrame()
        table_frame.setObjectName("glassPanel")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(18, 18, 18, 18)
        table_layout.setSpacing(12)
        table_title = QLabel("Completed Scans")
        table_title.setObjectName("sectionTitle")
        self.history_table = HistoryTable()
        table_layout.addWidget(table_title)
        table_layout.addWidget(self.history_table)
        layout.addWidget(table_frame)
        layout.addStretch()

        self.search_box.textChanged.connect(self._search)
        self.filter_button.clicked.connect(self.filter_requested.emit)
        self.export_button.clicked.connect(self.export_requested.emit)

    def _search(self, text):
        self.history_table.filter_rows(text)
        self.search_requested.emit(text)
