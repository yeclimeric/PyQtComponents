"""Responsive layout demo — three-panel layout with auto-folding."""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit,
)
from PySide6.QtCore import Qt

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.theme import ThemeManager
from pyqtcomponents.layout import ResponsiveLayout


def _make_panel(label: str, color: str) -> QWidget:
    w = QWidget()
    layout = QVBoxLayout(w)
    layout.addWidget(QLabel(label))
    text = QTextEdit(f"This is the {label.lower()} panel.\nResize the window to see auto-folding.")
    text.setReadOnly(True)
    layout.addWidget(text)
    w.setStyleSheet(f"background-color: {color};")
    return w


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Responsive Layout Demo")
        self.setMinimumSize(1024, 600)

        layout = ResponsiveLayout()
        layout.set_left_content(_make_panel("Left Panel", "#f0f4ff"))
        layout.set_center_content(_make_panel("Center Panel", "#ffffff"))
        layout.set_right_content(_make_panel("Right Panel", "#f0fff4"))
        self.setCentralWidget(layout)


def main():
    app = QApplication(sys.argv)
    theme = ThemeManager(mode="light")
    theme.apply(app)
    win = DemoWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
