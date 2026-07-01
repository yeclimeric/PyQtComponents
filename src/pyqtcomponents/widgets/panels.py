"""Styled panels — GroupBox, Card, Divider."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGroupBox, QFrame, QWidget, QVBoxLayout,
    QApplication,
)

from ..theme import tokens, spacing, typography


# ---------------------------------------------------------------------------
# QSS templates
# ---------------------------------------------------------------------------

_GROUP_BOX_QSS = """
QGroupBox {{
    font-size: {font_size}px;
    font-weight: bold;
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    margin-top: 8px;
    padding: {padding}px;
    padding-top: 16px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 4px;
    background-color: {bg};
}}
"""

_CARD_QSS = """
QFrame {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: {padding}px;
}}
QFrame:hover {{
    border-color: {border_hover};
}}
"""

_DIVIDER_QSS = """
QFrame {{
    background-color: {divider};
    border: none;
    min-height: 1px;
    max-height: 1px;
}}
"""


def _panel_css(dark: bool) -> dict:
    """Shared color dict for panel QSS."""
    return {
        "bg": "#ffffff" if not dark else tokens.NEUTRAL_800.name(),
        "fg": tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
        "border": tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_600.name(),
        "border_hover": tokens.NEUTRAL_300.name() if not dark else tokens.NEUTRAL_500.name(),
        "divider": tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_600.name(),
        "radius": 8,
        "padding": spacing.LG,
        "font_size": typography.SM,
    }


class StyledGroupBox(QGroupBox):
    """A themed group box with lightweight border and rounded corners.

    Per spec D7: border 1px neutral-200, radius 8px, padding 16px.
    """

    def __init__(self, title: str = "", parent=None):
        super().__init__(title, parent)
        self._apply_style()

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        self.setStyleSheet(_GROUP_BOX_QSS.format(**_panel_css(dark)))


class StyledCard(QFrame):
    """A themed card with border, rounded corners, and subtle hover effect.

    Per spec D7: border 1px neutral-200, radius 8px, shadow on hover.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        self.setStyleSheet(_CARD_QSS.format(**_panel_css(dark)))


class StyledDivider(QFrame):
    """A horizontal divider line.

    Per spec D7: color neutral-200, height 1px.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self._apply_style()

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        css = _panel_css(dark)
        self.setStyleSheet(_DIVIDER_QSS.format(divider=css["divider"]))
