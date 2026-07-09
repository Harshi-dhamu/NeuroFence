import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("NeuroFence")
window.resize(1200, 700)

window.show()

sys.exit(app.exec())