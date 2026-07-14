from datetime import datetime

from PyQt6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget


class ActivityWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Recent Activity")
        title.setObjectName("cardTitle")
        subtitle = QLabel("Live scanner workflow and security events")
        subtitle.setObjectName("cardDescription")

        self.list = QListWidget()
        self.list.setObjectName("activityList")
        self.add_activity("NeuroFence initialized")
        self.add_activity("Waiting for model")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.list, 1)

    def add_activity(self, text):
        item = QListWidgetItem(f"{datetime.now().strftime('%H:%M:%S')}   {text}")
        self.list.addItem(item)
        self.list.scrollToBottom()
