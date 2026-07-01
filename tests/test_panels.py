"""Smoke tests for styled panel components."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.widgets.panels import StyledGroupBox, StyledCard, StyledDivider


def test_groupbox_instantiate(qtbot):
    w = StyledGroupBox("Group Title")
    qtbot.addWidget(w)
    assert w.title() == "Group Title"


def test_groupbox_empty(qtbot):
    w = StyledGroupBox()
    qtbot.addWidget(w)
    assert w.title() == ""


def test_card_instantiate(qtbot):
    w = StyledCard()
    qtbot.addWidget(w)
    assert w is not None


def test_card_with_children(qtbot):
    from PySide6.QtWidgets import QLabel, QVBoxLayout
    w = StyledCard()
    qtbot.addWidget(w)
    layout = QVBoxLayout(w)
    layout.addWidget(QLabel("Hello"))
    layout.addWidget(QLabel("World"))
    assert w.findChild(QLabel) is not None


def test_divider_instantiate(qtbot):
    w = StyledDivider()
    qtbot.addWidget(w)
    assert w is not None
