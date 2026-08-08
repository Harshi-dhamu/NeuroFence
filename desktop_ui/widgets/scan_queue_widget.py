from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QHBoxLayout,
)


class ScanQueueWidget(QWidget):

    start_requested = pyqtSignal()
    remove_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Scan Queue")
        title.setObjectName("sectionTitle")

        self.queue_list = QListWidget()

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Queue")
        self.remove_button = QPushButton("Remove Selected")

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.remove_button)

        layout.addWidget(title)
        layout.addWidget(self.queue_list)
        layout.addLayout(button_layout)

        self.start_button.clicked.connect(
            self.start_requested.emit
        )

        self.remove_button.clicked.connect(
            self.remove_requested.emit
        )

    def add_model(self, model_path):
        self.queue_list.addItem(model_path)

    def remove_selected(self):
        row = self.queue_list.currentRow()

        if row >= 0:
            self.queue_list.takeItem(row)

    def get_next_model(self):
        if self.queue_list.count() == 0:
            return None

        item = self.queue_list.takeItem(0)

        return item.text()