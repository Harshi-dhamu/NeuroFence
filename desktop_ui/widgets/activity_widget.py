from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QListWidget,
    QVBoxLayout,
)


class ActivityWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setLayout(layout)

        title = QLabel("Recent Activity")

        title.setStyleSheet("""

            color:#58A6FF;
            font-size:18px;
            font-weight:bold;

        """)

        layout.addWidget(title)

        self.list = QListWidget()

        self.list.addItem("NeuroFence initialized")

        self.list.addItem("Waiting for model")

        layout.addWidget(self.list)

    def add_activity(self, text):

        self.list.addItem(text)

        self.list.scrollToBottom()