from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class DashboardChart(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Threat Score Trend")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        self.values = [12, 18, 35, 28, 45, 32, 60]

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        pen = QPen(QColor(0, 200, 255))
        pen.setWidth(3)

        painter.setPen(pen)

        if len(self.values) < 2:
            return

        w = self.width()
        h = self.height()

        margin = 30

        step = (w - (margin * 2)) / (len(self.values) - 1)

        max_value = max(self.values)

        points = []

        for i, value in enumerate(self.values):

            x = margin + (i * step)

            y = h - margin - (
                (value / max_value)
                * (h - (margin * 2))
            )

            points.append((x, y))

        for i in range(len(points) - 1):

            painter.drawLine(
                int(points[i][0]),
                int(points[i][1]),
                int(points[i + 1][0]),
                int(points[i + 1][1]),
            )