"""Reusable labelled report section for the detailed scan report page."""
from __future__ import annotations
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

class ReportSection(QFrame):
    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("ReportSection")
        self._rows: dict[str, tuple[QLabel, QLabel]] = {}
        layout = QVBoxLayout(self); layout.setContentsMargins(22,20,22,22); layout.setSpacing(14)
        heading = QLabel(title); heading.setObjectName("sectionTitle"); layout.addWidget(heading)
        self.grid = QGridLayout(); self.grid.setHorizontalSpacing(28); self.grid.setVerticalSpacing(12); layout.addLayout(self.grid)

    def set_data(self, values: dict[str, object]) -> None:
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._rows.clear()
        for row, (name, value) in enumerate(values.items()):
            key = QLabel(str(name)); key.setObjectName("reportKey")
            val = QLabel(str(value)); val.setObjectName("reportValue"); val.setWordWrap(True)
            self.grid.addWidget(key,row,0); self.grid.addWidget(val,row,1)
            self.grid.setColumnStretch(1,1); self._rows[name]=(key,val)
