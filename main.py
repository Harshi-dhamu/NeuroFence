import sys

from PyQt6.QtWidgets import QApplication

from desktop_ui.ui.main_window import MainWindow
from desktop_ui.themes.dark_theme import apply_dark_theme


def main():
    app = QApplication(sys.argv)

    apply_dark_theme(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()