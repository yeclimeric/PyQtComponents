"""Shared fixtures for tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest
from pyqtcomponents.layout.responsive import QSettings, SETTINGS_ORG, SETTINGS_APP


@pytest.fixture(autouse=True)
def clear_layout_settings():
    """Clear persisted layout settings before each test."""
    s = QSettings(SETTINGS_ORG, SETTINGS_APP)
    s.clear()
    yield
    s.clear()
