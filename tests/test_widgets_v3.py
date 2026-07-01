"""Smoke tests for widgets v3."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.widgets.widgets_v3 import (
    Tag, SegmentedControl, StatCard, EmptyState, SkeletonLoader,
    Rate, TreeView, BackToTop, Watermark,
)


def test_tag_instantiate(qtbot):
    t = Tag("Python")
    qtbot.addWidget(t)
    assert t.text() == "Python"


def test_tag_closable(qtbot):
    t = Tag("React", closable=True)
    qtbot.addWidget(t)
    t.closed.emit()


def test_tag_variants(qtbot):
    for v in ["default", "primary", "success", "warning", "error"]:
        t = Tag(v, variant=v)
        qtbot.addWidget(t)


def test_segmented_control_instantiate(qtbot):
    seg = SegmentedControl(["A", "B", "C"])
    qtbot.addWidget(seg)
    assert seg.current_index() == 0


def test_segmented_control_click(qtbot):
    seg = SegmentedControl(["X", "Y", "Z"])
    qtbot.addWidget(seg)
    seg._on_click(2)
    assert seg.current_index() == 2


def test_stat_card_instantiate(qtbot):
    card = StatCard("Users", "12,345", "+12%")
    qtbot.addWidget(card)


def test_stat_card_set_value(qtbot):
    card = StatCard("Revenue", "$0")
    qtbot.addWidget(card)
    card.set_value("$10,000")
    assert card._value.text() == "$10,000"


def test_empty_state_instantiate(qtbot):
    e = EmptyState("No results", "Try a different search.")
    qtbot.addWidget(e)


def test_skeleton_loader_instantiate(qtbot):
    s = SkeletonLoader(lines=5)
    qtbot.addWidget(s)
    s.stop()
    s.start()


def test_rate_instantiate(qtbot):
    r = Rate(max_stars=5, rating=3)
    qtbot.addWidget(r)
    assert r.rating == 3


def test_rate_set_rating(qtbot):
    r = Rate()
    qtbot.addWidget(r)
    r.rating = 4
    assert r.rating == 4


def test_tree_view_instantiate(qtbot):
    tree = TreeView()
    qtbot.addWidget(tree)
    tree.setHeaderLabels(["Name", "Type"])


def test_tree_view_add_items(qtbot):
    from PySide6.QtWidgets import QTreeWidgetItem
    tree = TreeView()
    qtbot.addWidget(tree)
    tree.setHeaderLabels(["Name"])
    parent = QTreeWidgetItem(tree, ["Folder"])
    QTreeWidgetItem(parent, ["File 1"])
    QTreeWidgetItem(parent, ["File 2"])
    assert tree.topLevelItemCount() == 1


def test_back_to_top_instantiate(qtbot):
    btt = BackToTop()
    qtbot.addWidget(btt)


def test_watermark_instantiate(qtbot):
    w = Watermark("DRAFT")
    qtbot.addWidget(w)
    w.set_text("FINAL")
    assert w._text == "FINAL"
