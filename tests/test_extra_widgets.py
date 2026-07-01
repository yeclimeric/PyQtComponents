"""Smoke tests for extra widgets."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.widgets.extra_widgets import (
    Cascader, StyledSwitch, CollapsiblePanel, Drawer,
    NavigationBar, TabPagination,
)


def test_cascader_instantiate(qtbot):
    c = Cascader()
    qtbot.addWidget(c)
    assert c.value == ""


def test_cascader_set_options(qtbot):
    c = Cascader()
    qtbot.addWidget(c)
    c.set_options({"Fruits": {"Apple": "apple", "Banana": "banana"}})
    assert len(c._options) == 1


def test_switch_instantiate(qtbot):
    s = StyledSwitch()
    qtbot.addWidget(s)
    assert s.checked is False


def test_switch_toggle(qtbot):
    s = StyledSwitch()
    qtbot.addWidget(s)
    s.toggle()
    assert s.checked is True
    s.toggle()
    assert s.checked is False


def test_switch_set_checked(qtbot):
    s = StyledSwitch(checked=True)
    qtbot.addWidget(s)
    assert s.checked is True


def test_collapsible_panel_instantiate(qtbot):
    p = CollapsiblePanel("Title")
    qtbot.addWidget(p)
    assert p is not None


def test_collapsible_panel_toggle(qtbot):
    p = CollapsiblePanel("Title")
    qtbot.addWidget(p)
    assert p._expanded is True
    p.toggle()
    assert p._expanded is False
    p.toggle()
    assert p._expanded is True


def test_collapsible_panel_add_content(qtbot):
    from PySide6.QtWidgets import QLabel
    p = CollapsiblePanel("Title")
    qtbot.addWidget(p)
    p.add_content(QLabel("Content"))


def test_drawer_instantiate(qtbot):
    from PySide6.QtWidgets import QMainWindow
    win = QMainWindow()
    qtbot.addWidget(win)
    win.show()
    d = Drawer(parent=win)
    assert d._open is False


def test_drawer_toggle(qtbot):
    from PySide6.QtWidgets import QMainWindow
    win = QMainWindow()
    qtbot.addWidget(win)
    win.resize(800, 600)
    win.show()
    d = Drawer(parent=win)
    d.open()
    assert d._open is True
    d.close()
    assert d._open is False


def test_navigation_bar_instantiate(qtbot):
    nav = NavigationBar()
    qtbot.addWidget(nav)
    assert nav.current_index() == -1


def test_navigation_bar_add_item(qtbot):
    nav = NavigationBar()
    qtbot.addWidget(nav)
    nav.add_item("home", "Home")
    nav.add_item("settings", "Settings")
    assert nav.current_index() == 0
    assert len(nav._buttons) == 2


def test_navigation_bar_click(qtbot):
    nav = NavigationBar()
    qtbot.addWidget(nav)
    nav.add_item("home", "Home")
    nav.add_item("settings", "Settings")
    nav._on_click(1)
    assert nav.current_index() == 1


def test_tab_pagination_instantiate(qtbot):
    pag = TabPagination(total_pages=5)
    qtbot.addWidget(pag)
    assert pag.current_page() == 0
    assert len(pag._buttons) == 5


def test_tab_pagination_click(qtbot):
    pag = TabPagination(total_pages=3)
    qtbot.addWidget(pag)
    pag._on_click(2)
    assert pag.current_page() == 2


def test_tab_pagination_set_total(qtbot):
    pag = TabPagination(total_pages=3)
    qtbot.addWidget(pag)
    pag.set_total_pages(5)
    assert len(pag._buttons) == 5
