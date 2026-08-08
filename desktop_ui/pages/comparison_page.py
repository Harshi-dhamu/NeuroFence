from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QGridLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ComparisonPage(QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWidgetResizable(True)

        content = QWidget()
        self.setWidget(content)

        self.layout = QVBoxLayout(content)

        title = QLabel("Scan Comparison")
        title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            """
        )

        self.layout.addWidget(title)

        self.comparison_frame = QFrame()
        self.grid = QGridLayout(self.comparison_frame)

        self.layout.addWidget(self.comparison_frame)

    def load_comparison(
        self,
        current_scan,
        previous_scan,
    ):
        while self.grid.count():
            item = self.grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        headers = [
            "Metric",
            "Previous Scan",
            "Current Scan",
        ]

        for col, text in enumerate(headers):
            label = QLabel(text)

            label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            label.setStyleSheet(
                """
                font-weight: bold;
                font-size: 14px;
                """
            )

            self.grid.addWidget(
                label,
                0,
                col,
            )

        rows = [
            (
                "Model",
                previous_scan.model_name,
                current_scan.model_name,
            ),
            (
                "Threat Score",
                str(previous_scan.threat_score),
                str(current_scan.threat_score),
            ),
            (
                "Risk Level",
                previous_scan.risk_level,
                current_scan.risk_level,
            ),
            (
                "Layers",
                str(previous_scan.layers),
                str(current_scan.layers),
            ),
            (
                "Framework",
                previous_scan.framework,
                current_scan.framework,
            ),
            (
                "Status",
                previous_scan.overall_status,
                current_scan.overall_status,
            ),
        ]

        for row_index, row_data in enumerate(rows, start=1):

            for col_index, value in enumerate(row_data):

                label = QLabel(value)

                label.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                label.setMinimumHeight(35)

                self.grid.addWidget(
                    label,
                    row_index,
                    col_index,
                )