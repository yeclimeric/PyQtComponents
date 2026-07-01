"""ThemeManager — builds QPalette from tokens, manages light/dark mode."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QFont
from PySide6.QtWidgets import QApplication

from . import tokens, typography


class ThemeManager:
    """Central theme coordinator.

    Usage::

        theme = ThemeManager()          # auto mode (reads OS palette)
        theme.apply(app)                # sets Fusion style + palette

        theme.color("text-primary")     # mode-aware lookup
        theme.set_mode("dark")          # explicit switch
    """

    def __init__(self, mode: str = "auto"):
        self._mode = mode
        self._dark = False
        self._resolve_mode()

    # -- public API -----------------------------------------------------------

    def apply(self, app: QApplication) -> None:
        """Apply Fusion style and build the application palette."""
        app.setStyle("Fusion")
        self._rebuild_palette(app)

    def color(self, token: str) -> QColor:
        """Look up a semantic color token for the current mode."""
        return tokens.semantic(token, dark=self._dark)

    def set_mode(self, mode: str, app: QApplication | None = None) -> None:
        """Switch mode ('auto' | 'light' | 'dark') and optionally re-apply."""
        if mode not in ("auto", "light", "dark"):
            raise ValueError(f"mode must be 'auto', 'light', or 'dark', got {mode!r}")
        self._mode = mode
        self._resolve_mode()
        if app is not None:
            self._rebuild_palette(app)

    @property
    def is_dark(self) -> bool:
        return self._dark

    # -- internal -------------------------------------------------------------

    def _resolve_mode(self) -> None:
        if self._mode == "auto":
            app = QApplication.instance()
            if app is not None:
                self._dark = app.palette().window().color().lightness() < 128
            else:
                self._dark = False
        else:
            self._dark = self._mode == "dark"

    def _rebuild_palette(self, app: QApplication) -> None:
        pal = QPalette()

        bg = tokens.semantic("background-primary", self._dark)
        bg_alt = tokens.semantic("background-secondary", self._dark)
        fg = tokens.semantic("text-primary", self._dark)
        fg_dim = tokens.semantic("text-secondary", self._dark)
        border = tokens.semantic("border-default", self._dark)
        highlight = tokens.semantic("highlight-focus", self._dark)

        # Window / Base
        pal.setColor(QPalette.Window, bg)
        pal.setColor(QPalette.WindowText, fg)
        pal.setColor(QPalette.Base, bg)
        pal.setColor(QPalette.AlternateBase, bg_alt)
        pal.setColor(QPalette.ToolTipBase, bg_alt)
        pal.setColor(QPalette.ToolTipText, fg)

        # Text
        pal.setColor(QPalette.Text, fg)
        pal.setColor(QPalette.Button, bg)
        pal.setColor(QPalette.ButtonText, fg)

        # Links
        pal.setColor(QPalette.Link, highlight)

        # Selection
        pal.setColor(QPalette.Highlight, highlight)
        pal.setColor(QPalette.HighlightedText, QColor("#ffffff"))

        # Disabled
        pal.setColor(QPalette.Disabled, QPalette.WindowText, fg_dim)
        pal.setColor(QPalette.Disabled, QPalette.Text, fg_dim)
        pal.setColor(QPalette.Disabled, QPalette.ButtonText, fg_dim)

        app.setPalette(pal)

        # Set a sensible default font
        font = QFont()
        font.setFamilies([typography.SANS_SERIF.split(",")[0].strip("'")])
        font.setPointSize(typography.BASE)
        app.setFont(font)
