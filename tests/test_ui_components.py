"""Smoke tests for UI components."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.widgets.ui_components import (
    Breadcrumb, Steps, Badge, Alert, Timeline, TransferList,
)


def test_breadcrumb_instantiate(qtbot):
    bc = Breadcrumb()
    qtbot.addWidget(bc)
    assert bc is not None


def test_breadcrumb_set_items(qtbot):
    bc = Breadcrumb()
    qtbot.addWidget(bc)
    bc.set_items(["Home", "Settings", "Advanced"])
    assert len(bc._labels) == 3


def test_steps_instantiate(qtbot):
    s = Steps()
    qtbot.addWidget(s)
    assert s is not None


def test_steps_set_steps(qtbot):
    s = Steps()
    qtbot.addWidget(s)
    s.set_steps(["Upload", "Process", "Done"])
    assert len(s._steps) == 3


def test_steps_set_current(qtbot):
    s = Steps()
    qtbot.addWidget(s)
    s.set_steps(["A", "B", "C"])
    s.set_current(1)
    assert s._current == 1


def test_badge_instantiate(qtbot):
    b = Badge("3")
    qtbot.addWidget(b)
    assert b.text() == "3"


def test_badge_variant(qtbot):
    for v in ["default", "primary", "success", "warning", "error"]:
        b = Badge("1", variant=v)
        qtbot.addWidget(b)


def test_alert_instantiate(qtbot):
    a = Alert("info", "Hello")
    qtbot.addWidget(a)
    assert a is not None


def test_alert_variants(qtbot):
    for v in ["info", "success", "warning", "error"]:
        a = Alert(v, f"Test {v}")
        qtbot.addWidget(a)


def test_alert_set_text(qtbot):
    a = Alert("info", "Original")
    qtbot.addWidget(a)
    a.set_text("Updated")
    assert a._label.text() == "Updated"


def test_timeline_instantiate(qtbot):
    t = Timeline()
    qtbot.addWidget(t)
    assert t is not None


def test_timeline_add_event(qtbot):
    t = Timeline()
    qtbot.addWidget(t)
    t.add_event("Event 1", "Desc 1")
    t.add_event("Event 2", "Desc 2")
    assert len(t._events) == 2


def test_timeline_clear(qtbot):
    t = Timeline()
    qtbot.addWidget(t)
    t.add_event("X")
    t.clear_events()
    assert len(t._events) == 0


def test_transfer_list_instantiate(qtbot):
    tl = TransferList()
    qtbot.addWidget(tl)
    assert tl is not None


def test_transfer_list_set_items(qtbot):
    tl = TransferList()
    qtbot.addWidget(tl)
    tl.set_source_items(["A", "B", "C"])
    tl.set_target_items(["D", "E"])
    assert len(tl.source_items()) == 3
    assert len(tl.target_items()) == 2
