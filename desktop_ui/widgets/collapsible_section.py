from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)


class CollapsibleSection(QWidget):

    def __init__(self, title, content_widget):
        super().__init__()

        self.content_widget = content_widget

        layout = QVBoxLayout(self)

        self.toggle_button = QPushButton(
            f"▼ {title}"
        )

        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)

        self.toggle_button.clicked.connect(
            self.toggle_content
        )

        layout.addWidget(self.toggle_button)
        layout.addWidget(content_widget)

    def toggle_content(self):

        expanded = self.toggle_button.isChecked()

        self.content_widget.setVisible(expanded)

        title = self.toggle_button.text()[2:]

        if expanded:
            self.toggle_button.setText(
                f"▼ {title}"
            )
        else:
            self.toggle_button.setText(
                f"▶ {title}"
            )