"""Smoke tests for StyledButton."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.widgets.button import StyledButton


def test_instantiate_primary(qtbot):
    btn = StyledButton("Click", level="primary")
    qtbot.addWidget(btn)
    assert btn.text() == "Click"
    assert btn.level == "primary"


def test_instantiate_secondary(qtbot):
    btn = StyledButton("Cancel", level="secondary")
    qtbot.addWidget(btn)
    assert btn.level == "secondary"


def test_instantiate_tertiary(qtbot):
    btn = StyledButton("Learn more", level="tertiary")
    qtbot.addWidget(btn)
    assert btn.level == "tertiary"


def test_instantiate_danger(qtbot):
    btn = StyledButton("Delete", level="danger")
    qtbot.addWidget(btn)
    assert btn.level == "danger"


def test_sizes(qtbot):
    for size in ("compact", "standard", "loose"):
        btn = StyledButton(size.title(), size=size)
        qtbot.addWidget(btn)
        assert btn.size == size


def test_change_level(qtbot):
    btn = StyledButton("Test", level="primary")
    qtbot.addWidget(btn)
    btn.level = "danger"
    assert btn.level == "danger"


def test_change_size(qtbot):
    btn = StyledButton("Test", size="compact")
    qtbot.addWidget(btn)
    btn.size = "loose"
    assert btn.size == "loose"


def test_invalid_level_raises(qtbot):
    import pytest
    with pytest.raises(ValueError, match="Unknown button level"):
        StyledButton("Bad", level="invalid")


def test_disabled_state(qtbot):
    btn = StyledButton("Disabled", level="primary")
    qtbot.addWidget(btn)
    btn.setEnabled(False)
    assert not btn.isEnabled()
