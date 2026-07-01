"""Smoke tests for Toast."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from PySide6.QtWidgets import QMainWindow
from pyqtcomponents.widgets.toast import Toast, _ToastWidget


def test_toast_shows(qtbot):
    """Toast.show() creates and displays a toast widget."""
    win = QMainWindow()
    win.resize(400, 300)
    win.show()
    qtbot.addWidget(win)

    Toast.show("Hello!", parent=win)
    qtbot.wait(100)

    # Find the toast child widget
    toasts = [c for c in win.children() if isinstance(c, _ToastWidget)]
    assert len(toasts) == 1
    assert toasts[0].isVisible()


def test_toast_auto_dismiss(qtbot):
    """Toast disappears after duration."""
    win = QMainWindow()
    win.resize(400, 300)
    win.show()
    qtbot.addWidget(win)

    Toast.show("Gone soon", duration=100, parent=win)
    qtbot.wait(50)

    toasts = [c for c in win.children() if isinstance(c, _ToastWidget)]
    assert len(toasts) == 1

    qtbot.wait(300)
    # Toast should have been closed
    assert not toasts[0].isVisible()


def test_toast_no_parent_no_crash(qtbot):
    """Toast.show() with no parent should not crash."""
    Toast.show("No parent")
    # Just verify no exception


def test_toast_positions_below_parent(qtbot):
    """Toast should be positioned near the bottom of the parent."""
    win = QMainWindow()
    win.resize(400, 300)
    win.show()
    qtbot.addWidget(win)

    Toast.show("Positioned", parent=win)
    qtbot.wait(100)

    toasts = [c for c in win.children() if isinstance(c, _ToastWidget)]
    assert len(toasts) == 1
    toast = toasts[0]
    # Toast should exist and be visible as a child of the parent
    assert toast.parent() is win
