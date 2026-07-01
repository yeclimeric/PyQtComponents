"""Smoke tests for PlotTheme."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.theme.plot import PlotTheme, PlotConfig, DATA_LINE_COLORS
from PySide6.QtGui import QColor


def test_plot_theme_instantiate(qtbot):
    theme = PlotTheme()
    assert theme is not None


def test_plot_light_config(qtbot):
    theme = PlotTheme()
    cfg = theme.light()
    assert isinstance(cfg, PlotConfig)
    assert cfg.background == QColor("#ffffff")
    assert cfg.grid_opacity == 0.3


def test_plot_dark_config(qtbot):
    theme = PlotTheme()
    cfg = theme.dark()
    assert isinstance(cfg, PlotConfig)
    assert cfg.background == QColor("#2d2d2d")
    assert cfg.grid_opacity == 0.3


def test_data_line_colors_count(qtbot):
    assert len(DATA_LINE_COLORS) == 7


def test_line_color_cycling(qtbot):
    theme = PlotTheme()
    cfg = theme.light()
    # Should cycle through colors
    c0 = cfg.line_color(0)
    c7 = cfg.line_color(7)
    assert c0 == c7  # wraps around


def test_grid_opacity(qtbot):
    theme = PlotTheme()
    cfg = theme.light()
    assert 0.0 <= cfg.grid_opacity <= 1.0
