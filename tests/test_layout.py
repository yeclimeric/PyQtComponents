"""Smoke tests for ResponsiveLayout."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from PySide6.QtWidgets import QLabel, QMainWindow
from pyqtcomponents.layout.responsive import (
    ResponsiveLayout, FOLD_LEFT, FOLD_RIGHT,
)


def test_responsive_layout_instantiate(qtbot):
    win = QMainWindow()
    win.resize(1200, 800)
    qtbot.addWidget(win)
    layout = ResponsiveLayout(win)
    win.setCentralWidget(layout)
    assert not layout.is_left_folded
    assert not layout.is_right_folded


def test_set_contents(qtbot):
    win = QMainWindow()
    win.resize(1200, 800)
    qtbot.addWidget(win)
    layout = ResponsiveLayout(win)
    win.setCentralWidget(layout)
    layout.set_left_content(QLabel("Left"))
    layout.set_center_content(QLabel("Center"))
    layout.set_right_content(QLabel("Right"))


def test_fold_left(qtbot):
    win = QMainWindow()
    win.resize(1200, 800)
    qtbot.addWidget(win)
    layout = ResponsiveLayout(win)
    win.setCentralWidget(layout)
    layout.set_left_content(QLabel("Left"))
    layout._toggle_left()
    assert layout.is_left_folded


def test_fold_right(qtbot):
    win = QMainWindow()
    win.resize(1200, 800)
    qtbot.addWidget(win)
    layout = ResponsiveLayout(win)
    win.setCentralWidget(layout)
    layout.set_right_content(QLabel("Right"))
    layout._toggle_right()
    assert layout.is_right_folded


def test_unfold_left(qtbot):
    # Clear any persisted fold state
    from pyqtcomponents.layout.responsive import QSettings, SETTINGS_ORG, SETTINGS_APP
    s = QSettings(SETTINGS_ORG, SETTINGS_APP)
    s.clear()

    win = QMainWindow()
    win.resize(1200, 800)
    qtbot.addWidget(win)
    layout = ResponsiveLayout(win)
    win.setCentralWidget(layout)
    layout._toggle_left()
    layout._toggle_left()
    assert not layout.is_left_folded


def test_fold_constants(qtbot):
    assert FOLD_LEFT == 700
    assert FOLD_RIGHT == 900
