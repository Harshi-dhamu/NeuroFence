from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFileDialog
)
from PyQt6.QtCore import Qt


class UploadCard(QWidget):
    def __init__(self):
        super().__init__()

        self.model_path = ""

        self.setObjectName("card")

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("📂 Upload LLM Model")
        title.setObjectName("cardTitle")

        description = QLabel(
            "Choose a HuggingFace or local model to begin analysis."
        )
        description.setWordWrap(True)
        description.setObjectName("cardDescription")

        self.path_label = QLabel("No model selected")
        self.path_label.setObjectName("pathLabel")

        self.button = QPushButton("Browse Model")
        self.button.setObjectName("primaryButton")
        self.button.clicked.connect(self.select_model)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.path_label)
        layout.addWidget(self.button)
        layout.addStretch()

        self.setLayout(layout)

    def select_model(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Model Folder"
        )

        if folder:
            self.model_path = folder
            self.path_label.setText(folder)
            