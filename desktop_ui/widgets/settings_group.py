"""Reusable settings card with labelled controls."""
from PyQt6.QtWidgets import QFrame,QGridLayout,QLabel,QVBoxLayout,QWidget
class SettingsGroup(QFrame):
    def __init__(self,title:str,description:str="",parent=None):
        super().__init__(parent); self.setObjectName("SettingsGroup")
        root=QVBoxLayout(self); root.setContentsMargins(22,20,22,22); root.setSpacing(12)
        heading=QLabel(title); heading.setObjectName("sectionTitle"); root.addWidget(heading)
        if description:
            desc=QLabel(description); desc.setObjectName("pageSubtitle"); desc.setWordWrap(True); root.addWidget(desc)
        self.grid=QGridLayout(); self.grid.setHorizontalSpacing(24); self.grid.setVerticalSpacing(14); self.grid.setColumnStretch(0,1); root.addLayout(self.grid); self._row=0
    def add_setting(self,label:str,control:QWidget,description:str=""):
        box=QVBoxLayout(); name=QLabel(label); name.setObjectName("settingName"); box.addWidget(name)
        if description:
            desc=QLabel(description); desc.setObjectName("settingDescription"); desc.setWordWrap(True); box.addWidget(desc)
        self.grid.addLayout(box,self._row,0); self.grid.addWidget(control,self._row,1); self._row+=1
