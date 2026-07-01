"""Styled dialogs — MessageBox, InputDialog."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMessageBox, QInputDialog, QLineEdit,
    QApplication,
)

from ..theme import tokens, typography


# ---------------------------------------------------------------------------
# Shared QSS
# ---------------------------------------------------------------------------

_DIALOG_QSS = """
QMessageBox, QInputDialog {{
    background-color: {bg};
    color: {fg};
}}
QMessageBox QLabel {{
    color: {fg};
    font-size: {font_size}px;
}}
QInputDialog QLabel {{
    color: {fg};
    font-size: {font_size}px;
}}
QInputDialog QLineEdit {{
    background-color: {input_bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: {pad}px;
    font-size: {font_size}px;
    min-height: {height}px;
}}
QInputDialog QLineEdit:focus {{
    border: 1px solid {accent};
}}
QPushButton {{
    background-color: {btn_bg};
    color: {btn_fg};
    border: 1px solid {btn_border};
    border-radius: {radius}px;
    padding: {pad}px {pad_h}px;
    font-size: {font_size}px;
    min-height: {height}px;
}}
QPushButton:hover {{
    background-color: {btn_hover};
}}
QPushButton:pressed {{
    background-color: {btn_pressed};
}}
"""


def _dialog_css(dark: bool) -> dict:
    """Shared color dict for dialog QSS."""
    return {
        "bg": "#ffffff" if not dark else tokens.NEUTRAL_800.name(),
        "fg": tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
        "border": tokens.NEUTRAL_300.name() if not dark else tokens.NEUTRAL_600.name(),
        "input_bg": "#ffffff" if not dark else tokens.NEUTRAL_700.name(),
        "accent": tokens.PRIMARY_500.name() if not dark else tokens.PRIMARY_400.name(),
        "btn_bg": tokens.PRIMARY_600.name() if not dark else tokens.PRIMARY_500.name(),
        "btn_fg": "#ffffff",
        "btn_border": tokens.PRIMARY_600.name() if not dark else tokens.PRIMARY_500.name(),
        "btn_hover": tokens.PRIMARY_700.name() if not dark else tokens.PRIMARY_400.name(),
        "btn_pressed": tokens.PRIMARY_800.name() if not dark else tokens.PRIMARY_300.name(),
        "radius": 4,
        "pad": 8,
        "pad_h": 16,
        "height": 32,
        "font_size": typography.BASE,
    }


class StyledMessageBox:
    """Themed message box with static convenience methods.

    Usage::

        StyledMessageBox.info("Title", "Message", parent=window)
        StyledMessageBox.warning("Title", "Warning!", parent=window)
        StyledMessageBox.error("Title", "Error occurred", parent=window)
        result = StyledMessageBox.question("Title", "Proceed?", parent=window)
    """

    @staticmethod
    def _apply_style(box: QMessageBox) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        box.setStyleSheet(_DIALOG_QSS.format(**_dialog_css(dark)))

    @staticmethod
    def info(title: str, text: str, parent=None) -> None:
        """Show an informational message box."""
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle(title)
        box.setText(text)
        StyledMessageBox._apply_style(box)
        box.exec()

    @staticmethod
    def warning(title: str, text: str, parent=None) -> None:
        """Show a warning message box."""
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle(title)
        box.setText(text)
        StyledMessageBox._apply_style(box)
        box.exec()

    @staticmethod
    def error(title: str, text: str, parent=None) -> None:
        """Show an error message box."""
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Icon.Critical)
        box.setWindowTitle(title)
        box.setText(text)
        StyledMessageBox._apply_style(box)
        box.exec()

    @staticmethod
    def question(title: str, text: str, parent=None) -> bool:
        """Show a question dialog. Returns True if Yes is clicked."""
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Icon.Question)
        box.setWindowTitle(title)
        box.setText(text)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        box.setDefaultButton(QMessageBox.StandardButton.No)
        StyledMessageBox._apply_style(box)
        return box.exec() == QMessageBox.StandardButton.Yes


class StyledInputDialog:
    """Themed input dialog with static convenience methods.

    Usage::

        text = StyledInputDialog.text("Title", "Enter name:", parent=window)
        num, ok = StyledInputDialog.integer("Title", "Enter age:", parent=window)
        num, ok = StyledInputDialog.double("Title", "Enter value:", parent=window)
    """

    @staticmethod
    def _apply_style(dialog: QInputDialog) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        dialog.setStyleSheet(_DIALOG_QSS.format(**_dialog_css(dark)))

    @staticmethod
    def text(title: str, label: str, parent=None, default: str = "") -> str | None:
        """Show a text input dialog. Returns the text or None if cancelled."""
        text, ok = QInputDialog.getText(parent, title, label, text=default)
        return text if ok else None

    @staticmethod
    def integer(
        title: str, label: str, parent=None,
        value: int = 0, min_val: int = 0, max_val: int = 999,
    ) -> tuple[int, bool]:
        """Show an integer input dialog. Returns (value, ok)."""
        val, ok = QInputDialog.getInt(parent, title, label, value, min_val, max_val)
        return val, ok

    @staticmethod
    def double(
        title: str, label: str, parent=None,
        value: float = 0.0, min_val: float = 0.0, max_val: float = 999.0,
        decimals: int = 2,
    ) -> tuple[float, bool]:
        """Show a double input dialog. Returns (value, ok)."""
        val, ok = QInputDialog.getDouble(
            parent, title, label, value, min_val, max_val, decimals
        )
        return val, ok

    @staticmethod
    def choice(
        title: str, label: str, choices: list[str], parent=None,
    ) -> str | None:
        """Show a choice input dialog. Returns the selected item or None."""
        item, ok = QInputDialog.getItem(parent, title, label, choices)
        return item if ok else None
