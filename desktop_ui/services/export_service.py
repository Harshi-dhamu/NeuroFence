"""Day 10 report building and local export framework."""
from __future__ import annotations
import csv, json
from pathlib import Path
from typing import Any
from desktop_ui.models.scan_result import ScanResult

class ExportService:
    def build_report(self,result: ScanResult) -> dict[str,Any]:
        """Normalize ScanResult for display/export; replace or extend for backend reports later."""
        return result.to_dict()
    def export_json(self,result: ScanResult,path: str) -> Path:
        target=Path(path); target.write_text(json.dumps(self.build_report(result),indent=2,default=str),encoding="utf-8"); return target
    def export_csv(self,result: ScanResult,path: str) -> Path:
        target=Path(path); flat=self._flatten(self.build_report(result))
        with target.open("w",newline="",encoding="utf-8") as handle:
            writer=csv.writer(handle); writer.writerow(["Field","Value"]); writer.writerows(flat.items())
        return target
    def export_pdf(self,result: ScanResult,path: str) -> Path:
        """Placeholder PDF hook. Real PDF renderer will be added after final report format is frozen."""
        raise NotImplementedError("PDF export framework is prepared; connect the final PDF renderer here.")
    def save_report(self,result: ScanResult,path: str) -> Path:
        return self.export_json(result,path)
    def _flatten(self,data: dict[str,Any],prefix: str="") -> dict[str,Any]:
        output={}
        for key,value in data.items():
            name=f"{prefix}.{key}" if prefix else key
            if isinstance(value,dict): output.update(self._flatten(value,name))
            elif isinstance(value,list): output[name]="; ".join(map(str,value))
            else: output[name]=value
        return output
