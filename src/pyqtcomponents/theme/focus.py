"""Focus indicator styles and keyboard navigation helpers.

Per spec D12:
- All interactive elements must be Tab-reachable
- Visible focus indicator (2px outline)
- Logical Tab order
- Shortcut hints
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget, QApplication

from . import tokens


# ---------------------------------------------------------------------------
# Focus QSS templates
# ---------------------------------------------------------------------------

_FOCUS_QSS = """
QWidget:focus {{
    outline: none;
}}
QPushButton:focus, QToolButton:focus {{
    border: 2px solid {focus_color};
    outline: none;
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border: 1px solid {focus_color};
    outline: none;
}}
QCheckBox:focus, QRadioButton:focus {{
    outline: none;
}}
QCheckBox:focus-visible::indicator, QRadioButton:focus-visible::indicator {{
    border: 2px solid {focus_color};
}}
"""


def focus_qss(dark: bool = False) -> str:
    """Return QSS for focus indicators."""
    focus_color = tokens.PRIMARY_400.name() if dark else tokens.PRIMARY_500.name()
    return _FOCUS_QSS.format(focus_color=focus_color)


def apply_focus_style(widget: QWidget) -> None:
    """Apply focus indicator styles to a widget or its parent."""
    app = QApplication.instance()
    dark = False
    if app is not None:
        dark = app.palette().window().color().lightness() < 128
    widget.setStyleSheet(focus_qss(dark))


class FocusTracker:
    """Track and manage focus order across widgets.

    Usage::

        tracker = FocusTracker()
        tracker.register(widget1, order=0)
        tracker.register(widget2, order=1)
        tracker.focus_next()  # moves to widget2
    """

    def __init__(self):
        self._widgets: list[QWidget] = []
        self._order: dict[int, QWidget] = {}

    def register(self, widget: QWidget, order: int | None = None) -> None:
        """Register a widget for focus tracking."""
        if widget not in self._widgets:
            self._widgets.append(widget)
        if order is not None:
            self._order[order] = widget

    def focus_next(self) -> None:
        """Move focus to the next widget in order."""
        current = QApplication.focusWidget()
        if current in self._widgets:
            idx = self._widgets.index(current)
            next_idx = (idx + 1) % len(self._widgets)
            self._widgets[next_idx].setFocus()
        elif self._widgets:
            self._widgets[0].setFocus()

    def focus_previous(self) -> None:
        """Move focus to the previous widget in order."""
        current = QApplication.focusWidget()
        if current in self._widgets:
            idx = self._widgets.index(current)
            prev_idx = (idx - 1) % len(self._widgets)
            self._widgets[prev_idx].setFocus()
        elif self._widgets:
            self._widgets[-1].setFocus()
