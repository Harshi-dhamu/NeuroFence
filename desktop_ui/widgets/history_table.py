"""Professional scan history table with filtering and append support."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem


class HistoryTable(QTableWidget):
    HEADERS = ["Scan ID", "Model", "Date", "Threat Score", "Result"]

    def __init__(self, parent=None):
        super().__init__(0, len(self.HEADERS), parent)
        self.setObjectName("HistoryTable")
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setMinimumHeight(390)
        self._seed_samples()

    def _seed_samples(self):
        samples = [
            ("NF-0024", "TinyLlama", "14 Jul 2026 · 10:45 AM", "18%", "SAFE"),
            ("NF-0023", "Phi-3 Mini", "13 Jul 2026 · 04:18 PM", "12%", "SAFE"),
            ("NF-0022", "Model-Audit-v2", "12 Jul 2026 · 11:07 AM", "64%", "SUSPICIOUS"),
            ("NF-0021", "Gemma 2B", "11 Jul 2026 · 03:30 PM", "9%", "SAFE"),
            ("NF-0020", "Llama Test Build", "10 Jul 2026 · 09:12 AM", "37%", "REVIEW"),
        ]
        for row in samples:
            self.add_scan(*row)

    def add_scan(self, scan_id, model, date, threat_score, result):
        self.insertRow(0)
        values = [scan_id, model, date, threat_score, result]
        for column, value in enumerate(values):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | (Qt.AlignmentFlag.AlignCenter if column in (0, 3, 4) else Qt.AlignmentFlag.AlignLeft))
            if column == 4:
                item.setData(Qt.ItemDataRole.UserRole, str(result).lower())
            self.setItem(0, column, item)
        self.setRowHeight(0, 48)

    def filter_rows(self, query):
        query = query.strip().lower()
        for row in range(self.rowCount()):
            visible = not query or any(query in (self.item(row, col).text().lower() if self.item(row, col) else "") for col in range(self.columnCount()))
            self.setRowHidden(row, not visible)
