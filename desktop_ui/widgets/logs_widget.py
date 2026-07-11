from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout


class LogsWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("card")

        layout = QVBoxLayout()

        title = QLabel("📜 Live Logs")
        title.setObjectName("cardTitle")

        self.logs = QTextEdit()

        self.logs.setReadOnly(True)

        self.logs.append("NeuroFence initialized...")
        self.logs.append("Waiting for model upload...")
        self.logs.append("Ready.")

        layout.addWidget(title)
        layout.addWidget(self.logs)

        self.setLayout(layout)

    def add_log(self, message):

        self.logs.append(message)