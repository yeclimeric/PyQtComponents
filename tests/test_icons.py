"""Smoke tests for IconProvider."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.icons import IconProvider, ICON_XS, ICON_SM, ICON_MD, ICON_LG
from pyqtcomponents.icons.provider import SIZE_MAP


def test_icon_provider_instantiate(qtbot):
    provider = IconProvider()
    assert provider is not None


def test_icon_size_constants(qtbot):
    assert ICON_XS == 12
    assert ICON_SM == 16
    assert ICON_MD == 24
    assert ICON_LG == 32


def test_icon_size_map(qtbot):
    assert SIZE_MAP["xs"] == 12
    assert SIZE_MAP["sm"] == 16
    assert SIZE_MAP["md"] == 24
    assert SIZE_MAP["lg"] == 32


def test_get_icon(qtbot):
    provider = IconProvider()
    icon = provider.get("file", size="md")
    assert icon is not None
    assert not icon.isNull()


def test_get_pixmap(qtbot):
    provider = IconProvider()
    pixmap = provider.get_pixmap("file", size="sm")
    assert pixmap is not None
    assert pixmap.width() == 16
    assert pixmap.height() == 16


def test_list_icons(qtbot):
    provider = IconProvider()
    icons = provider.list_icons()
    assert "file" in icons
    assert "folder" in icons
    assert "search" in icons
    assert "settings" in icons
    assert "check" in icons
    assert "close" in icons


def test_icon_caching(qtbot):
    provider = IconProvider()
    p1 = provider.get_pixmap("file", size="md")
    p2 = provider.get_pixmap("file", size="md")
    assert p1 is p2  # same object from cache


def test_unknown_icon_returns_empty(qtbot):
    provider = IconProvider()
    pixmap = provider.get_pixmap("nonexistent", size="md")
    assert pixmap is not None
    assert pixmap.width() == 24
