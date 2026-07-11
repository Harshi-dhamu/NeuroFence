from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class InfoCard(QWidget):

    def __init__(self, title, value):

        super().__init__()

        layout = QVBoxLayout()

        heading = QLabel(title)

        heading.setObjectName("cardTitle")

        number = QLabel(value)

        number.setObjectName("cardValue")

        layout.addWidget(heading)

        layout.addWidget(number)

        self.setLayout(layout)