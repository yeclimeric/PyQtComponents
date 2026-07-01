"""Smoke tests for extra styled widgets."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from PySide6.QtCore import Qt
from pyqtcomponents.widgets.extras import StyledProgressBar, StyledSlider, StyledTabWidget
from PySide6.QtWidgets import QLabel


def test_progress_bar_instantiate(qtbot):
    w = StyledProgressBar()
    qtbot.addWidget(w)
    w.setRange(0, 100)
    assert w.minimum() == 0
    assert w.maximum() == 100


def test_progress_bar_set_value(qtbot):
    w = StyledProgressBar()
    qtbot.addWidget(w)
    w.setValue(50)
    assert w.value() == 50


def test_progress_bar_range(qtbot):
    w = StyledProgressBar()
    qtbot.addWidget(w)
    w.setRange(0, 100)
    w.setValue(75)
    assert w.value() == 75


def test_slider_instantiate(qtbot):
    w = StyledSlider()
    qtbot.addWidget(w)
    assert w.value() == 0


def test_slider_set_value(qtbot):
    w = StyledSlider()
    qtbot.addWidget(w)
    w.setRange(0, 100)
    w.setValue(42)
    assert w.value() == 42


def test_slider_orientation(qtbot):
    w = StyledSlider(Qt.Orientation.Vertical)
    qtbot.addWidget(w)
    assert w.orientation() == Qt.Orientation.Vertical


def test_tab_widget_instantiate(qtbot):
    w = StyledTabWidget()
    qtbot.addWidget(w)
    assert w.count() == 0


def test_tab_widget_add_tabs(qtbot):
    w = StyledTabWidget()
    qtbot.addWidget(w)
    w.addTab(QLabel("Tab 1"), "First")
    w.addTab(QLabel("Tab 2"), "Second")
    assert w.count() == 2


def test_tab_widget_current(qtbot):
    w = StyledTabWidget()
    qtbot.addWidget(w)
    w.addTab(QLabel("A"), "Alpha")
    w.addTab(QLabel("B"), "Beta")
    w.setCurrentIndex(1)
    assert w.currentIndex() == 1
