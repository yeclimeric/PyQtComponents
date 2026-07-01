"""Advanced styled widgets — Tooltip, Table, MenuBar."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QToolTip, QTableWidget, QTableWidgetItem, QHeaderView,
    QMenuBar, QMenu, QWidget,
    QApplication,
)

from ..theme import tokens, spacing, typography


# ---------------------------------------------------------------------------
# Tooltip QSS
# ---------------------------------------------------------------------------

_TOOLTIP_QSS = """
QToolTip {{
    background-color: {bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: {pad}px;
    font-size: {font_size}px;
}}
"""


class StyledTooltip:
    """Themed tooltip helper.

    Usage::

        StyledTooltip.set_text(widget, "Tooltip text")
    """

    @staticmethod
    def set_text(widget: QWidget, text: str) -> None:
        """Set tooltip text on a widget."""
        widget.setToolTip(text)


# ---------------------------------------------------------------------------
# Table QSS
# ---------------------------------------------------------------------------

_TABLE_QSS = """
QTableWidget {{
    background-color: {bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    gridline-color: {gridline};
    font-size: {font_size}px;
    selection-background-color: {selection};
}}
QTableWidget::item {{
    padding: {pad}px;
}}
QTableWidget::item:selected {{
    background-color: {selection};
    color: {fg};
}}
QHeaderView::section {{
    background-color: {header_bg};
    color: {fg};
    border: none;
    border-bottom: 1px solid {border};
    border-right: 1px solid {border};
    padding: {pad}px;
    font-weight: bold;
    font-size: {font_size}px;
}}
"""


class StyledTable(QTableWidget):
    """A themed table with styled headers and selection."""

    def __init__(self, rows: int = 0, columns: int = 0, parent=None):
        super().__init__(rows, columns, parent)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self._apply_style()

    def set_headers(self, headers: list[str]) -> None:
        """Set horizontal header labels."""
        self.setHorizontalHeaderLabels(headers)
        for i, h in enumerate(headers):
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents
            )

    def add_row(self, values: list[str]) -> None:
        """Add a row with the given values."""
        row = self.rowCount()
        self.insertRow(row)
        for col, val in enumerate(values):
            item = QTableWidgetItem(val)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, col, item)

    def clear_rows(self) -> None:
        """Remove all rows."""
        self.setRowCount(0)

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        self.setStyleSheet(_TABLE_QSS.format(
            bg="#ffffff" if not dark else tokens.NEUTRAL_800.name(),
            fg=tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
            border=tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_600.name(),
            gridline=tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_700.name(),
            header_bg=tokens.NEUTRAL_100.name() if not dark else tokens.NEUTRAL_700.name(),
            selection=tokens.PRIMARY_100.name() if not dark else tokens.PRIMARY_900.name(),
            radius=4,
            pad=spacing.SM,
            font_size=typography.BASE,
        ))


# ---------------------------------------------------------------------------
# MenuBar QSS
# ---------------------------------------------------------------------------

_MENUBAR_QSS = """
QMenuBar {{
    background-color: {bg};
    color: {fg};
    border-bottom: 1px solid {border};
    font-size: {font_size}px;
}}
QMenuBar::item {{
    padding: {pad}px {pad_h}px;
    background-color: transparent;
}}
QMenuBar::item:selected {{
    background-color: {hover};
}}
QMenu {{
    background-color: {bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: {pad}px;
}}
QMenu::item {{
    padding: {pad}px {pad_h}px;
    border-radius: 3px;
}}
QMenu::item:selected {{
    background-color: {hover};
}}
"""


class StyledMenuBar(QMenuBar):
    """A themed menu bar with styled menus."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()

    def add_menu(self, title: str) -> QMenu:
        """Add a menu and return it."""
        menu = self.addMenu(title)
        menu.setStyleSheet(self.styleSheet())
        return menu

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128
        css = _MENUBAR_QSS.format(
            bg="#ffffff" if not dark else tokens.NEUTRAL_800.name(),
            fg=tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
            border=tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_600.name(),
            hover=tokens.NEUTRAL_100.name() if not dark else tokens.NEUTRAL_700.name(),
            radius=4,
            pad=spacing.SM,
            pad_h=spacing.MD,
            font_size=typography.BASE,
        )
        self.setStyleSheet(css)
