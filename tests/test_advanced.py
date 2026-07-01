"""Smoke tests for advanced styled widgets."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.widgets.advanced import StyledTooltip, StyledTable, StyledMenuBar


def test_tooltip_set_text(qtbot):
    from PySide6.QtWidgets import QPushButton
    btn = QPushButton("Test")
    qtbot.addWidget(btn)
    StyledTooltip.set_text(btn, "Hello tooltip")
    assert btn.toolTip() == "Hello tooltip"


def test_table_instantiate(qtbot):
    w = StyledTable(3, 2)
    qtbot.addWidget(w)
    assert w.rowCount() == 3
    assert w.columnCount() == 2


def test_table_set_headers(qtbot):
    w = StyledTable(0, 2)
    qtbot.addWidget(w)
    w.set_headers(["Name", "Value"])
    assert w.horizontalHeaderItem(0).text() == "Name"
    assert w.horizontalHeaderItem(1).text() == "Value"


def test_table_add_row(qtbot):
    w = StyledTable(0, 2)
    qtbot.addWidget(w)
    w.set_headers(["A", "B"])
    w.add_row(["x", "y"])
    assert w.rowCount() == 1
    assert w.item(0, 0).text() == "x"
    assert w.item(0, 1).text() == "y"


def test_table_clear_rows(qtbot):
    w = StyledTable(0, 2)
    qtbot.addWidget(w)
    w.add_row(["1", "2"])
    w.add_row(["3", "4"])
    w.clear_rows()
    assert w.rowCount() == 0


def test_menubar_instantiate(qtbot):
    from PySide6.QtWidgets import QMainWindow
    win = QMainWindow()
    qtbot.addWidget(win)
    menu = StyledMenuBar(win)
    win.setMenuBar(menu)
    assert menu is not None


def test_menubar_add_menu(qtbot):
    from PySide6.QtWidgets import QMainWindow
    win = QMainWindow()
    qtbot.addWidget(win)
    menu = StyledMenuBar(win)
    win.setMenuBar(menu)
    file_menu = menu.add_menu("File")
    assert file_menu is not None
    assert len(menu.actions()) == 1
