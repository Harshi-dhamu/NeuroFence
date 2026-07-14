from PyQt6.QtWidgets import QApplication


def get_dark_theme():
    return r"""
    QMainWindow, QWidget#mainCentralWidget, QWidget#dashboardWidget, QScrollArea, QScrollArea > QWidget > QWidget {
        background: #07111F;
    }
    QWidget {
        color: #D7E2F0;
        font-family: "Segoe UI";
        font-size: 10.5pt;
    }
    QScrollBar:vertical { background:#07111F; width:10px; margin:0; }
    QScrollBar::handle:vertical { background:#26364A; min-height:42px; border-radius:5px; }
    QScrollBar::handle:vertical:hover { background:#36506C; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }

    QFrame#sidebar {
        background: #0B1727;
        border: none;
        border-right: 1px solid #1D2A3B;
    }
    QLabel#brandMark {
        background: #0EA5E9;
        color: #03111F;
        border-radius: 12px;
        font-weight: 900;
        font-size: 15pt;
    }
    QLabel#logo { color:#F8FAFC; font-size:20pt; font-weight:800; padding:0; }
    QLabel#sidebarCaption, QLabel#eyebrow, QLabel#miniCaption {
        color:#64748B; font-size:8pt; font-weight:700; letter-spacing:1px;
    }
    QLabel#sidebarFooter {
        color:#64748B; font-size:9pt; background:#0F1D30; border:1px solid #1D2A3B;
        border-radius:10px; padding:12px;
    }
    QPushButton#navButton {
        background:transparent; color:#94A3B8; border:none; border-radius:9px;
        padding:12px 14px; text-align:left; font-weight:600;
    }
    QPushButton#navButton:hover { background:#11243A; color:#E2E8F0; }
    QPushButton#navButton:checked { background:#0D3150; color:#7DD3FC; border-left:3px solid #38BDF8; }

    QFrame#TopBar, QWidget#card, QFrame#RecentScanPanel, QFrame#SystemStatusCard, QFrame#SystemInfo {
        background:#0D1B2D;
        border:1px solid #1F3147;
        border-radius:16px;
    }
    QFrame#TopBar { border-top:2px solid #0EA5E9; }
    QFrame#headerMiniCard { background:#0A1625; border:1px solid #1D3046; border-radius:12px; }
    QLabel#heroTitle { color:#F8FAFC; font-size:23pt; font-weight:800; }
    QLabel#heroSubtitle { color:#94A3B8; font-size:10pt; }
    QLabel#clockValue { color:#E0F2FE; font-size:16pt; font-weight:700; }
    QLabel#headerStatus { color:#2DD4BF; font-size:16px; font-weight:700; }

    QLabel#cardTitle { color:#E8F3FF; font-size:15pt; font-weight:700; }
    QLabel#cardDescription { color:#8292A8; font-size:9.5pt; }
    QLabel#cardValue { color:#F8FAFC; font-size:23pt; font-weight:800; }
    QLabel#metricIcon { background:#0B2940; color:#38BDF8; border:1px solid #164B6B; border-radius:12px; font-size:18pt; font-weight:700; }
    QLabel#metricTitle { color:#8EA0B8; font-size:9.5pt; font-weight:600; }
    QLabel#metricSubtitle { color:#64748B; font-size:8.5pt; }

    QLabel#pathLabel {
        background:#081422; border:1px dashed #31506F; border-radius:9px;
        color:#9FB2C8; padding:10px;
    }
    QLabel#statusReady { color:#2DD4BF; font-weight:700; font-size:10.5pt; }
    QLabel#progressStage { color:#BAE6FD; font-weight:600; }

    QPushButton#primaryButton, QPushButton#scanButton {
        color:#F8FAFC; border:none; border-radius:10px; padding:12px 16px; font-weight:700;
    }
    QPushButton#primaryButton { background:#0F766E; }
    QPushButton#primaryButton:hover { background:#0D9488; }
    QPushButton#scanButton { background:#0369A1; }
    QPushButton#scanButton:hover { background:#0284C7; }
    QPushButton#scanButton:disabled { background:#24435A; color:#7990A4; }
    QPushButton#secondaryButton {
        background:#11243A; color:#AFC0D3; border:1px solid #294058;
        border-radius:8px; padding:7px 12px; font-weight:600;
    }
    QPushButton#secondaryButton:hover { background:#17304C; color:#F8FAFC; }

    QProgressBar#securityProgress {
        background:#081422; border:1px solid #25394F; border-radius:8px;
        height:24px; color:#E2E8F0; text-align:center; font-weight:700;
    }
    QProgressBar#securityProgress::chunk { background:#0EA5E9; border-radius:7px; }

    QListWidget#activityList, QTextEdit#securityConsole {
        background:#07131F; border:1px solid #1E3044; border-radius:10px;
        color:#C7D4E3; padding:8px; selection-background-color:#123B58;
    }
    QListWidget#activityList::item { padding:8px; border-bottom:1px solid #132238; }
    QListWidget#activityList::item:hover { background:#0E2034; }
    QTextEdit#securityConsole { font-family:"Cascadia Mono", Consolas, monospace; font-size:9.5pt; }
    QLabel#logCounter { color:#5EEAD4; background:#0B2A2B; border:1px solid #155E5A; border-radius:8px; padding:6px 9px; font-size:8pt; font-weight:700; }

    QSplitter::handle { background:#07111F; }
    QSplitter::handle:hover { background:#17304C; }

    QMenuBar { background:#0B1727; color:#B7C5D6; border-bottom:1px solid #1D2A3B; }
    QMenuBar::item { padding:7px 10px; }
    QMenuBar::item:selected { background:#11243A; color:#F8FAFC; }
    QMenu { background:#0D1B2D; color:#D7E2F0; border:1px solid #26394F; }
    QMenu::item:selected { background:#0D3150; }
    QStatusBar { background:#0B1727; color:#7F93AA; border-top:1px solid #1D2A3B; }
    QMessageBox { background:#0D1B2D; }
    """


def apply_dark_theme(app: QApplication):
    app.setStyleSheet(get_dark_theme())
