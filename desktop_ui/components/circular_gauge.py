from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import (
    QPainter,
    QPen,
    QColor,
    QFont,
)
from PyQt6.QtCore import Qt, QRectF


class CircularGauge(QWidget):

    def __init__(self):
        super().__init__()

        self.value = 5          # Threat %
        self.maximum = 100

        self.setMinimumSize(250, 250)

    ##########################################################

    def setValue(self, value):

        self.value = max(0, min(value, self.maximum))

        self.update()

    ##########################################################

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        ##################################################
        # Background
        ##################################################

        painter.fillRect(self.rect(), QColor("#161B22"))

        ##################################################
        # Circle Area
        ##################################################

        size = min(self.width(), self.height()) - 40

        rect = QRectF(
            (self.width() - size) / 2,
            (self.height() - size) / 2,
            size,
            size
        )

        ##################################################
        # Background Ring
        ##################################################

        pen = QPen()

        pen.setWidth(14)

        pen.setColor(QColor("#30363D"))

        painter.setPen(pen)

        painter.drawArc(rect, 0, 360 * 16)

        ##################################################
        # Progress Ring
        ##################################################

        if self.value < 30:
            color = "#3FB950"      # Green

        elif self.value < 70:
            color = "#F2CC60"      # Yellow

        else:
            color = "#F85149"      # Red

        pen.setColor(QColor(color))

        painter.setPen(pen)

        span = int((self.value / self.maximum) * 360)

        painter.drawArc(
            rect,
            90 * 16,
            -span * 16
        )

        ##################################################
        # Percentage
        ##################################################

        painter.setPen(Qt.GlobalColor.white)

        painter.setFont(
            QFont(
                "Segoe UI",
                28,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            f"{self.value}%"
        )

        ##################################################
        # Title
        ##################################################

        painter.setFont(
            QFont(
                "Segoe UI",
                12
            )
        )

        painter.setPen(QColor("#58A6FF"))

        painter.drawText(
            0,
            35,
            self.width(),
            30,
            Qt.AlignmentFlag.AlignCenter,
            "Threat Score"
        )

        ##################################################
        # Status
        ##################################################

        if self.value < 30:

            status = "SAFE"

            color = "#3FB950"

        elif self.value < 70:

            status = "WARNING"

            color = "#F2CC60"

        else:

            status = "CRITICAL"

            color = "#F85149"

        painter.setPen(QColor(color))

        painter.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            0,
            self.height() - 35,
            self.width(),
            20,
            Qt.AlignmentFlag.AlignCenter,
            status
        )