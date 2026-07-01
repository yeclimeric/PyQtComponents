"""Tests for screen reader and accessibility support."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from PySide6.QtWidgets import QPushButton, QGroupBox
from pyqtcomponents.theme.accessibility import (
    set_accessible_name, set_accessible_description,
    set_accessible_properties,
    AccessibleGroup, AccessibleButton, AccessibleTable,
)


def test_set_accessible_name(qtbot):
    btn = QPushButton("Click")
    qtbot.addWidget(btn)
    set_accessible_name(btn, "Submit form")
    assert btn.accessibleName() == "Submit form"


def test_set_accessible_description(qtbot):
    btn = QPushButton("Click")
    qtbot.addWidget(btn)
    set_accessible_description(btn, "Submits the form to server")
    assert btn.accessibleDescription() == "Submits the form to server"


def test_set_accessible_properties(qtbot):
    btn = QPushButton("Click")
    qtbot.addWidget(btn)
    set_accessible_properties(btn, name="OK", description="Confirm action")
    assert btn.accessibleName() == "OK"
    assert btn.accessibleDescription() == "Confirm action"


def test_accessible_group(qtbot):
    group = AccessibleGroup("Settings")
    qtbot.addWidget(group)
    assert group.accessibleName() == "Settings"
    assert "Settings" in group.accessibleDescription()


def test_accessible_button(qtbot):
    btn = AccessibleButton("Save")
    qtbot.addWidget(btn)
    assert btn.accessibleName() == "Save"


def test_accessible_button_shortcut(qtbot):
    btn = AccessibleButton("Save")
    qtbot.addWidget(btn)
    btn.set_shortcut_hint("Ctrl+S")
    assert "Ctrl+S" in btn.accessibleDescription()


def test_accessible_table(qtbot):
    table = AccessibleTable(3, 2)
    qtbot.addWidget(table)
    table.setHorizontalHeaderLabels(["Name", "Value"])
    desc = table.accessibleDescription()
    assert "3 rows" in desc
    assert "2 columns" in desc
    assert "Name" in desc
    assert "Value" in desc
