"""Tests for focus indicators and keyboard navigation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from PySide6.QtWidgets import QPushButton, QLineEdit
from pyqtcomponents.theme.focus import (
    focus_qss, FocusTracker,
)


def test_focus_qss_light():
    css = focus_qss(dark=False)
    assert "3b82f6" in css  # primary-500


def test_focus_qss_dark():
    css = focus_qss(dark=True)
    assert "60a5fa" in css  # primary-400


def test_focus_tracker_register(qtbot):
    tracker = FocusTracker()
    btn1 = QPushButton("A")
    btn2 = QPushButton("B")
    qtbot.addWidget(btn1)
    qtbot.addWidget(btn2)
    tracker.register(btn1, order=0)
    tracker.register(btn2, order=1)
    assert len(tracker._widgets) == 2


def test_focus_tracker_no_duplicate(qtbot):
    tracker = FocusTracker()
    btn = QPushButton("A")
    qtbot.addWidget(btn)
    tracker.register(btn)
    tracker.register(btn)
    assert len(tracker._widgets) == 1


def test_focus_tracker_next(qtbot):
    from PySide6.QtWidgets import QApplication, QMainWindow
    win = QMainWindow()
    win.resize(400, 300)
    qtbot.addWidget(win)

    tracker = FocusTracker()
    btn1 = QPushButton("A", win)
    btn2 = QPushButton("B", win)
    win.show()
    qtbot.wait(100)

    tracker.register(btn1)
    tracker.register(btn2)

    btn1.setFocus()
    qtbot.wait(100)
    tracker.focus_next()
    qtbot.wait(100)
    focused = QApplication.instance().focusWidget()
    assert focused is btn2


def test_focus_tracker_previous(qtbot):
    from PySide6.QtWidgets import QApplication, QMainWindow
    win = QMainWindow()
    win.resize(400, 300)
    qtbot.addWidget(win)

    tracker = FocusTracker()
    btn1 = QPushButton("A", win)
    btn2 = QPushButton("B", win)
    win.show()
    qtbot.wait(50)

    tracker.register(btn1)
    tracker.register(btn2)

    btn2.setFocus()
    qtbot.wait(50)
    tracker.focus_previous()
    qtbot.wait(50)
    focused = QApplication.instance().focusWidget()
    assert focused is btn1
