"""StyledButton — QSS-themed QPushButton with level and size variants."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QApplication

from ..theme import tokens, spacing, typography

# ---------------------------------------------------------------------------
# QSS templates — parameterized by color values
# ---------------------------------------------------------------------------

_QSS_TEMPLATE = """
QPushButton {{
    background-color: {bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: {pad_v}px {pad_h}px;
    font-size: {font_size}px;
    min-height: {height}px;
}}
QPushButton:hover {{
    background-color: {bg_hover};
}}
QPushButton:pressed {{
    background-color: {bg_pressed};
}}
QPushButton:disabled {{
    background-color: {bg_disabled};
    color: {fg_disabled};
}}
QPushButton:focus {{
    outline: none;
    border: 2px solid {focus_ring};
}}
"""

_SIZE_MAP = {
    "compact":  {"height": 24, "pad_v": spacing.XS, "pad_h": spacing.SM + spacing.XS},
    "standard": {"height": 32, "pad_v": spacing.SM, "pad_h": spacing.LG},
    "loose":    {"height": 40, "pad_v": spacing.MD, "pad_h": spacing.XL},
}

_RADIUS = 4


def _level_colors(level: str, dark: bool) -> dict:
    """Return fill, hover, pressed, border colors for a button level."""
    if level == "primary":
        return {
            "bg": tokens.PRIMARY_600.name(),
            "fg": "#ffffff",
            "bg_hover": tokens.PRIMARY_700.name(),
            "bg_pressed": tokens.PRIMARY_800.name(),
            "border": tokens.PRIMARY_600.name(),
        }
    if level == "secondary":
        return {
            "bg": "#ffffff",
            "fg": tokens.NEUTRAL_700.name(),
            "bg_hover": tokens.NEUTRAL_50.name(),
            "bg_pressed": tokens.NEUTRAL_100.name(),
            "border": tokens.NEUTRAL_300.name(),
        }
    if level == "tertiary":
        return {
            "bg": "transparent",
            "fg": tokens.PRIMARY_600.name(),
            "bg_hover": "transparent",
            "bg_pressed": "transparent",
            "border": "transparent",
        }
    if level == "danger":
        return {
            "bg": tokens.ERROR.name(),
            "fg": "#ffffff",
            "bg_hover": "#dc2626",
            "bg_pressed": "#b91c1c",
            "border": tokens.ERROR.name(),
        }
    raise ValueError(f"Unknown button level: {level!r}")


class StyledButton(QPushButton):
    """A themed button with level and size variants.

    Levels: ``primary`` | ``secondary`` | ``tertiary`` | ``danger``
    Sizes:  ``compact`` | ``standard`` | ``loose``
    """

    def __init__(
        self,
        text: str = "",
        level: str = "primary",
        size: str = "standard",
        parent=None,
    ):
        super().__init__(text, parent)
        self._level = level
        self._size = size
        self._apply_style()

    # -- properties -----------------------------------------------------------

    @property
    def level(self) -> str:
        return self._level

    @level.setter
    def level(self, value: str) -> None:
        self._level = value
        self._apply_style()

    @property
    def size(self) -> str:
        return self._size

    @size.setter
    def size(self, value: str) -> None:
        self._size = value
        self._apply_style()

    # -- internal -------------------------------------------------------------

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            palette = app.palette()
            dark = palette.window().color().lightness() < 128

        colors = _level_colors(self._level, dark)
        dims = _SIZE_MAP[self._size]
        self.setStyleSheet(
            _QSS_TEMPLATE.format(
                radius=_RADIUS,
                font_size=typography.BASE,
                focus_ring=tokens.PRIMARY_400.name() if not dark else tokens.PRIMARY_300.name(),
                bg_disabled=tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_700.name(),
                fg_disabled=tokens.NEUTRAL_400.name() if not dark else tokens.NEUTRAL_500.name(),
                **colors,
                **dims,
            )
        )
