"""Toolbar for exporting or saving the currently displayed scan report."""
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame,QHBoxLayout,QLabel,QPushButton

class ExportToolbar(QFrame):
    export_json_requested=pyqtSignal(); export_csv_requested=pyqtSignal(); export_pdf_requested=pyqtSignal(); save_requested=pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent); self.setObjectName("glassToolbar")
        layout=QHBoxLayout(self); layout.setContentsMargins(16,12,16,12); layout.setSpacing(10)
        label=QLabel("Export report"); label.setObjectName("toolbarTitle"); layout.addWidget(label); layout.addStretch()
        for text, signal in (("Export JSON",self.export_json_requested),("Export CSV",self.export_csv_requested),("Export PDF",self.export_pdf_requested),("Save Report",self.save_requested)):
            button=QPushButton(text); button.setObjectName("secondaryButton"); button.clicked.connect(signal.emit); layout.addWidget(button)
