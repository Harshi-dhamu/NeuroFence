from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget


class UploadCard(QWidget):
    def __init__(self):
        super().__init__()
        self.model_path = ""
        self.setObjectName("card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(12)

        eyebrow = QLabel("MODEL INTAKE")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Upload LLM Model")
        title.setObjectName("cardTitle")
        description = QLabel("Choose a Hugging Face or local model directory for isolated security analysis.")
        description.setWordWrap(True)
        description.setObjectName("cardDescription")

        self.path_label = QLabel("No model selected")
        self.path_label.setObjectName("pathLabel")
        self.path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.button = QPushButton("Browse model directory")
        self.button.setObjectName("primaryButton")
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(self.select_model)

        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
        layout.addWidget(self.path_label)
        layout.addWidget(self.button)

    def select_model(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Model Folder")
        if folder:
            self.model_path = folder
            self.path_label.setText(folder)
