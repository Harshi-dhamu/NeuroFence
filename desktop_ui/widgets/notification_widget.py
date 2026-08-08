from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
)

from PyQt6.QtCore import Qt


class NotificationWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("card")

        layout = QVBoxLayout(self)

        title = QLabel("Notification Center")
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.notification_list = QListWidget()
        layout.addWidget(self.notification_list)

    def add_notification(self, message):
        item = QListWidgetItem(message)

        self.notification_list.insertItem(0, item)

        while self.notification_list.count() > 20:
            self.notification_list.takeItem(
                self.notification_list.count() - 1
            )