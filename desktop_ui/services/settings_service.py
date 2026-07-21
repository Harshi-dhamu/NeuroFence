"""Persistent application settings stored in config/app_settings.json."""
from __future__ import annotations
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

DEFAULT_SETTINGS={
 "general":{"auto_save_reports":True,"start_maximized":False,"enable_animations":True},
 "scanner":{"deep_scan":True,"activation_tracking":True,"prompt_fuzzing":True,"scan_timeout":120},
 "appearance":{"dark_theme":True,"accent_color":"Cyan","font_size":11},
 "logging":{"file_logging":False,"maximum_log_entries":500}
}
class SettingsService:
    def __init__(self,path: str|Path|None=None):
        self.path=Path(path) if path else Path(__file__).resolve().parents[1]/"config"/"app_settings.json"; self.path.parent.mkdir(parents=True,exist_ok=True)
    def load_settings(self)->dict[str,Any]:
        if not self.path.exists(): self.save_settings(DEFAULT_SETTINGS); return deepcopy(DEFAULT_SETTINGS)
        try:
            stored=json.loads(self.path.read_text(encoding="utf-8")); return self._merge(deepcopy(DEFAULT_SETTINGS),stored)
        except (OSError,json.JSONDecodeError): return deepcopy(DEFAULT_SETTINGS)
    def save_settings(self,settings:dict[str,Any])->None: self.path.write_text(json.dumps(settings,indent=2),encoding="utf-8")
    def reset_to_defaults(self)->dict[str,Any]:
        settings=deepcopy(DEFAULT_SETTINGS); self.save_settings(settings); return settings
    def _merge(self,base,update):
        for key,value in update.items():
            if isinstance(value,dict) and isinstance(base.get(key),dict): self._merge(base[key],value)
            else: base[key]=value
        return base
