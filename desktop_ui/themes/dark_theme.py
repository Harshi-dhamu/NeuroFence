def apply_dark_theme(app):

    app.setStyleSheet("""

        QMainWindow{

            background:#111111;

        }

        QWidget{

            background:#111111;

            color:white;

            font-family:Segoe UI;

        }

        QMenuBar{

            background:#181818;

            color:white;

        }

        QMenuBar::item:selected{

            background:#2D2D2D;

        }

        QStatusBar{

            background:#181818;

            color:white;

        }

    """)