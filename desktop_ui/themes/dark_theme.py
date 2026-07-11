
def get_dark_theme():
    return """
    /* ----------------------------- */
    /* Main Window                   */
    /* ----------------------------- */

    QMainWindow {
        background-color: #0D1117;
    }

    QWidget {
        background-color: #0D1117;
        color: #E6EDF3;
        font-family: Segoe UI;
        font-size: 11pt;
    }

    /* ----------------------------- */
    /* Sidebar                       */
    /* ----------------------------- */

    QWidget#sidebar {
        background-color: #161B22;
        border-right: 2px solid #30363D;
    }

    QLabel#logo {
        font-size: 22px;
        font-weight: bold;
        color: #58A6FF;
        padding: 10px;
    }

    QPushButton {
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 12px;
        text-align: left;
        color: white;
    }

    QPushButton:hover {
        background-color: #21262D;
    }

    QPushButton:pressed {
        background-color: #30363D;
    }

    /* ----------------------------- */
    /* Cards                         */
    /* ----------------------------- */

    QWidget#card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 15px;
    }

    QLabel#cardTitle {
        font-size: 16pt;
        font-weight: bold;
        color: #58A6FF;
    }

    QLabel#cardDescription {
        color: #9CA3AF;
        font-size: 10pt;
    }

    QLabel#cardValue {
        font-size: 24pt;
        font-weight: bold;
        color: white;
    }

    QLabel#pathLabel {
        background-color: #0D1117;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 8px;
        color: #C9D1D9;
    }

    QLabel#statusReady {
        color: #3FB950;
        font-weight: bold;
        font-size: 12pt;
    }

    /* ----------------------------- */
    /* Primary Buttons               */
    /* ----------------------------- */

    QPushButton#primaryButton {

        background-color: #238636;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px;
    }

    QPushButton#primaryButton:hover {

        background-color: #2EA043;
    }

    /* ----------------------------- */

    QPushButton#scanButton {

        background-color: #1F6FEB;
        color: white;
        font-weight: bold;
        font-size: 12pt;
        border-radius: 12px;
        padding: 15px;
    }

    QPushButton#scanButton:hover {

        background-color: #388BFD;
    }

    /* ----------------------------- */
    /* QTextEdit                     */
    /* ----------------------------- */

    QTextEdit {

        background-color: #0D1117;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 10px;
        color: #E6EDF3;
    }

    /* ----------------------------- */
    /* Status Bar                    */
    /* ----------------------------- */

    QStatusBar {

        background-color: #161B22;
        color: #8B949E;
    }

    /* ----------------------------- */
    /* Menu Bar                      */
    /* ----------------------------- */

    QMenuBar {

        background-color: #161B22;
        color: white;
    }

    QMenuBar::item:selected {

        background-color: #21262D;
    }

    QMenu {

        background-color: #161B22;
        color: white;
    }

    QMenu::item:selected {

        background-color: #238636;
    }
    """
from PyQt6.QtWidgets import QApplication


def apply_dark_theme(app: QApplication):
    app.setStyleSheet(get_dark_theme())