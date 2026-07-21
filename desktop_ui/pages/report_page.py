"""Scrollable detailed report viewer for a completed NeuroFence scan."""
from __future__ import annotations
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel,QScrollArea,QVBoxLayout,QWidget
from desktop_ui.components.export_toolbar import ExportToolbar
from desktop_ui.models.scan_result import ScanResult
from desktop_ui.widgets.recommendation_card import RecommendationCard
from desktop_ui.widgets.report_section import ReportSection

class ReportPage(QScrollArea):
    export_json_requested=pyqtSignal(); export_csv_requested=pyqtSignal(); export_pdf_requested=pyqtSignal(); save_requested=pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent); self.setObjectName("ReportPage"); self.setWidgetResizable(True); self.setFrameShape(QScrollArea.Shape.NoFrame)
        content=QWidget(); content.setObjectName("pageContent"); self.setWidget(content)
        layout=QVBoxLayout(content); layout.setContentsMargins(28,28,28,28); layout.setSpacing(20)
        title=QLabel("Scan Report"); title.setObjectName("pageTitle")
        subtitle=QLabel("Detailed model security analysis and export-ready findings"); subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title); layout.addWidget(subtitle)
        self.toolbar=ExportToolbar(); layout.addWidget(self.toolbar)
        self.summary=ReportSection("Scan Summary"); self.model=ReportSection("Model Details"); self.detection=ReportSection("Detection Results"); self.activation=ReportSection("Activation Analysis"); self.threat=ReportSection("Threat Assessment"); self.recommendations=RecommendationCard()
        for widget in (self.summary,self.model,self.detection,self.activation,self.threat,self.recommendations): layout.addWidget(widget)
        layout.addStretch()
        self.toolbar.export_json_requested.connect(self.export_json_requested); self.toolbar.export_csv_requested.connect(self.export_csv_requested); self.toolbar.export_pdf_requested.connect(self.export_pdf_requested); self.toolbar.save_requested.connect(self.save_requested)
        self.clear_report()
    def clear_report(self):
        self.summary.set_data({"Status":"No completed scan","Timestamp":"—"}); self.model.set_data({"Model":"—","Framework":"—","Architecture":"—"}); self.detection.set_data({"Summary":"Run a scan to populate this section."}); self.activation.set_data({"Summary":"Run a scan to populate this section."}); self.threat.set_data({"Threat Score":"0%","Risk Level":"Ready"}); self.recommendations.set_recommendations("Complete a scan to generate security recommendations.")
    def set_scan_result(self,result: ScanResult):
        self.summary.set_data({"Overall Status":result.overall_status,"Scan Duration":f"{result.scan_duration:.1f} seconds","Timestamp":result.timestamp,"Stages Completed":result.statistics.stages_completed})
        self.model.set_data({"Model Name":result.model_name,"Framework":result.framework,"Architecture":result.architecture,"File Size":f"{result.file_size_mb:.1f} MB","Layers":result.layers,"Source Path":result.model_path or "Demo provider"})
        self.detection.set_data({"Threat Score":f"{result.threat_score}%","Risk Level":result.risk_level.title(),"Suspicious Weights":result.detection.suspicious_weight_count,"Suspicious Prompts":", ".join(result.suspicious_prompts) or "None","Summary":result.detection_summary})
        self.activation.set_data({"Neurons Analysed":result.activation.neurons_analyzed,"Dead Neurons":result.activation.dead_neurons,"Anomalous Activations":result.activation.anomalous_activations,"Summary":result.activation_summary})
        self.threat.set_data({"Threat Score":f"{result.threat_score}%","Risk Level":result.risk_level.title(),"Final Result":result.overall_status})
        self.recommendations.set_recommendations(result.recommendation)
