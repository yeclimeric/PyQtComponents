"""Extra styled widgets — ProgressBar, Slider, TabWidget."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QProgressBar, QSlider, QTabWidget, QTabBar,
    QApplication, QWidget,
)

from ..theme import tokens, spacing, typography


# ---------------------------------------------------------------------------
# Shared QSS
# ---------------------------------------------------------------------------

_PROGRESS_QSS = """
QProgressBar {{
    background-color: {bg_track};
    border: none;
    border-radius: {radius}px;
    height: {height}px;
    text-align: center;
    color: {fg};
    font-size: {font_size}px;
}}
QProgressBar::chunk {{
    background-color: {accent};
    border-radius: {radius}px;
}}
"""

_SLIDER_QSS = """
QSlider::groove:horizontal {{
    background: {bg_track};
    height: 6px;
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {accent};
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}}
QSlider::handle:horizontal:hover {{
    background: {accent_hover};
}}
QSlider::sub-page:horizontal {{
    background: {accent};
    border-radius: 3px;
}}
"""

_TAB_QSS = """
QTabWidget::pane {{
    border: 1px solid {border};
    border-radius: {radius}px;
    background-color: {bg};
    padding: {padding}px;
}}
QTabBar::tab {{
    background-color: {bg_tab};
    color: {fg};
    border: 1px solid {border};
    border-bottom: none;
    border-radius: {radius}px {radius}px 0 0;
    padding: {pad_v}px {pad_h}px;
    font-size: {font_size}px;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background-color: {bg};
    color: {accent};
    font-weight: bold;
}}
QTabBar::tab:hover:!selected {{
    background-color: {bg_hover};
}}
"""


def _extras_css(dark: bool) -> dict:
    """Shared color dict for extras QSS."""
    return {
        "bg": "#ffffff" if not dark else tokens.NEUTRAL_800.name(),
        "fg": tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
        "border": tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_600.name(),
        "bg_track": tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_700.name(),
        "bg_tab": tokens.NEUTRAL_100.name() if not dark else tokens.NEUTRAL_800.name(),
        "bg_hover": tokens.NEUTRAL_50.name() if not dark else tokens.NEUTRAL_700.name(),
        "accent": tokens.PRIMARY_600.name() if not dark else tokens.PRIMARY_400.name(),
        "accent_hover": tokens.PRIMARY_700.name() if not dark else tokens.PRIMARY_300.name(),
        "radius": 4,
        "height": 8,
        "padding": spacing.LG,
        "pad_v": spacing.SM,
        "pad_h": spacing.MD,
        "font_size": typography.BASE,
    }


class StyledProgressBar(QProgressBar):
    """A themed progress bar with rounded corners."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)
        self.setMinimumHeight(8)
        self._apply_style()

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        self.setStyleSheet(_PROGRESS_QSS.format(**_extras_css(dark)))


class StyledSlider(QSlider):
    """A themed horizontal slider with round handle."""

    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self._apply_style()

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        self.setStyleSheet(_SLIDER_QSS.format(**_extras_css(dark)))


class StyledTabWidget(QTabWidget):
    """A themed tab widget with styled tab bar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()

    def addTab(self, widget: QWidget, label: str) -> int:
        """Add a tab with the given label."""
        return super().addTab(widget, label)

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        self.setStyleSheet(_TAB_QSS.format(**_extras_css(dark)))
