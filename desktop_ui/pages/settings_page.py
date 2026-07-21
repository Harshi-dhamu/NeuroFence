"""Persistent NeuroFence application settings page."""
from __future__ import annotations
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox,QHBoxLayout,QLabel,QPushButton,QScrollArea,QSpinBox,QVBoxLayout,QWidget
from desktop_ui.widgets.settings_group import SettingsGroup
from desktop_ui.widgets.toggle_switch import ToggleSwitch

class SettingsPage(QScrollArea):
    save_requested=pyqtSignal(dict); reset_requested=pyqtSignal(); clear_logs_requested=pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent); self.setObjectName("SettingsPage"); self.setWidgetResizable(True); self.setFrameShape(QScrollArea.Shape.NoFrame)
        content=QWidget(); content.setObjectName("pageContent"); self.setWidget(content); root=QVBoxLayout(content); root.setContentsMargins(28,28,28,28); root.setSpacing(20)
        title=QLabel("Settings & Preferences"); title.setObjectName("pageTitle"); root.addWidget(title)
        sub=QLabel("Configure NeuroFence appearance, scanning behaviour and logging preferences."); sub.setObjectName("pageSubtitle"); root.addWidget(sub)
        self.controls={}
        general=SettingsGroup("General"); self._toggle(general,"auto_save_reports","Auto-save reports","Save completed reports automatically."); self._toggle(general,"start_maximized","Start maximized","Open NeuroFence in maximized mode."); self._toggle(general,"enable_animations","Enable animations","Use page transition animations."); root.addWidget(general)
        scanner=SettingsGroup("Scanner"); self._toggle(scanner,"deep_scan","Enable deep scan","Store preference for the detection backend."); self._toggle(scanner,"activation_tracking","Enable activation tracking","Allow Akhina's module when integrated."); self._toggle(scanner,"prompt_fuzzing","Enable prompt fuzzing","Allow Dhruti's fuzzing workflow when integrated."); timeout=QSpinBox(); timeout.setRange(10,3600); timeout.setSuffix(" sec"); self.controls["scan_timeout"]=timeout; scanner.add_setting("Scan timeout",timeout,"Maximum time available to backend scans."); root.addWidget(scanner)
        appearance=SettingsGroup("Appearance"); self._toggle(appearance,"dark_theme","Dark theme","Use the enterprise dark interface."); accent=QComboBox(); accent.addItems(["Cyan","Teal","Blue","Purple"]); self.controls["accent_color"]=accent; appearance.add_setting("Accent color",accent,"Prepared for future theme variants."); font=QSpinBox(); font.setRange(9,18); font.setSuffix(" pt"); self.controls["font_size"]=font; appearance.add_setting("Font size",font); root.addWidget(appearance)
        logging=SettingsGroup("Logging"); self._toggle(logging,"file_logging","Enable file logging","Prepared for persistent security logs."); maximum=QSpinBox(); maximum.setRange(100,10000); maximum.setSingleStep(100); self.controls["maximum_log_entries"]=maximum; logging.add_setting("Maximum log entries",maximum); clear=QPushButton("Clear Logs"); clear.setObjectName("secondaryButton"); clear.clicked.connect(self.clear_logs_requested); logging.add_setting("Clear current logs",clear); root.addWidget(logging)
        actions=QHBoxLayout(); actions.addStretch(); reset=QPushButton("Reset Defaults"); reset.setObjectName("secondaryButton"); save=QPushButton("Save Settings"); save.setObjectName("primaryButton"); reset.clicked.connect(self.reset_requested); save.clicked.connect(lambda:self.save_requested.emit(self.collect_settings())); actions.addWidget(reset); actions.addWidget(save); root.addLayout(actions); root.addStretch()
    def _toggle(self,group,key,label,description): control=ToggleSwitch(); self.controls[key]=control; group.add_setting(label,control,description)
    def set_settings(self,s):
        mapping={**s["general"],**s["scanner"],**s["appearance"],**s["logging"]}
        for key,value in mapping.items():
            control=self.controls.get(key)
            if isinstance(control,ToggleSwitch): control.setChecked(bool(value))
            elif isinstance(control,QSpinBox): control.setValue(int(value))
            elif isinstance(control,QComboBox): control.setCurrentText(str(value))
    def collect_settings(self):
        def val(key):
            c=self.controls[key]
            if isinstance(c,ToggleSwitch): return c.isChecked()
            if isinstance(c,QSpinBox): return c.value()
            return c.currentText()
        return {"general":{k:val(k) for k in ("auto_save_reports","start_maximized","enable_animations")},"scanner":{k:val(k) for k in ("deep_scan","activation_tracking","prompt_fuzzing","scan_timeout")},"appearance":{k:val(k) for k in ("dark_theme","accent_color","font_size")},"logging":{k:val(k) for k in ("file_logging","maximum_log_entries")}}
