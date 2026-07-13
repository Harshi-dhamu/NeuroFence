import platform
import sys
import subprocess

from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QGridLayout
)

from PyQt6.QtGui import QFont

import PyQt6


class SystemInfo(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("SystemInfo")

        self.setup_ui()

    ########################################################

    def setup_ui(self):

        layout = QVBoxLayout()

        self.setLayout(layout)

        ####################################################
        # Title
        ####################################################

        title = QLabel("System Information")

        title.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))

        title.setStyleSheet("""
            color:#58A6FF;
        """)

        layout.addWidget(title)

        ####################################################

        grid = QGridLayout()

        grid.setHorizontalSpacing(30)

        grid.setVerticalSpacing(15)

        ####################################################
        # Left Labels
        ####################################################

        labels = [
            "Operating System",
            "Python Version",
            "PyQt Version",
            "Project Version",
            "Git Branch"
        ]

        values = [
            platform.system() + " " + platform.release(),
            platform.python_version(),
            PyQt6.QtCore.PYQT_VERSION_STR,
            "v1.0",
            self.get_branch()
        ]

        for i in range(len(labels)):

            label = QLabel(labels[i])

            label.setStyleSheet("""
                color:#8B949E;
                font-size:12px;
            """)

            value = QLabel(values[i])

            value.setStyleSheet("""
                color:white;
                font-size:13px;
                font-weight:bold;
            """)

            grid.addWidget(label, i, 0)

            grid.addWidget(value, i, 1)

        layout.addLayout(grid)

        layout.addStretch()

        ####################################################

        self.setStyleSheet("""

        QFrame#SystemInfo{

            background:#161B22;

            border:1px solid #30363D;

            border-radius:15px;

        }

        """)

    ########################################################

    def get_branch(self):

        try:

            branch = subprocess.check_output(
                ["git", "branch", "--show-current"],
                text=True
            ).strip()

            return branch

        except Exception:

            return "Unknown"