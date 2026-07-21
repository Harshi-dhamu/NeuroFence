"""Compact reusable boolean toggle implemented without third-party packages."""
from PyQt6.QtCore import Qt,pyqtSignal
from PyQt6.QtWidgets import QPushButton
class ToggleSwitch(QPushButton):
    toggled_value=pyqtSignal(bool)
    def __init__(self,checked=False,parent=None):
        super().__init__(parent); self.setObjectName("toggleSwitch"); self.setCheckable(True); self.setFixedSize(58,30); self.setCursor(Qt.CursorShape.PointingHandCursor); self.setChecked(checked); self.clicked.connect(self._emit); self._sync()
    def _emit(self,value): self._sync(); self.toggled_value.emit(bool(value))
    def _sync(self): self.setText("●" if self.isChecked() else "○"); self.setProperty("active",self.isChecked()); self.style().unpolish(self); self.style().polish(self)
    def setChecked(self,value): super().setChecked(value); self._sync() if hasattr(self,"style") else None
