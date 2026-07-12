from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
)


class ProgressCard(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setLayout(layout)

        title = QLabel("Scan Progress")

        title.setStyleSheet("""
            color:#58A6FF;
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.progress = QProgressBar()

        self.progress.setValue(0)

        self.progress.setStyleSheet("""

        QProgressBar{

            border:1px solid #30363D;
            border-radius:8px;
            background:#161B22;
            height:25px;

        }

        QProgressBar::chunk{

            background:#238636;
            border-radius:8px;

        }

        """)

        layout.addWidget(self.progress)