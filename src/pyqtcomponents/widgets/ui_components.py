"""UI components — Breadcrumb, Steps, Badge, Alert, Timeline, TransferList."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QListWidget, QListWidgetItem, QApplication,
)

from ..theme import tokens, spacing, typography


# ---------------------------------------------------------------------------
# Shared CSS
# ---------------------------------------------------------------------------

def _ui_css(dark: bool) -> dict:
    return {
        "bg": "#ffffff" if not dark else tokens.NEUTRAL_800.name(),
        "fg": tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
        "fg_dim": tokens.NEUTRAL_500.name() if not dark else tokens.NEUTRAL_400.name(),
        "border": tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_600.name(),
        "bg_hover": tokens.NEUTRAL_50.name() if not dark else tokens.NEUTRAL_700.name(),
        "accent": tokens.PRIMARY_600.name() if not dark else tokens.PRIMARY_400.name(),
        "accent_bg": tokens.PRIMARY_50.name() if not dark else tokens.PRIMARY_900.name(),
        "success": tokens.SUCCESS.name(),
        "warning": tokens.WARNING.name(),
        "error": tokens.ERROR.name(),
        "radius": 4,
        "pad": spacing.SM,
        "pad_h": spacing.MD,
        "font_size": typography.BASE,
        "font_sm": typography.SM,
    }


# ============================================================
# Breadcrumb
# ============================================================

class Breadcrumb(QWidget):
    """Horizontal breadcrumb navigation.

    Usage::

        bc = Breadcrumb()
        bc.set_items(["Home", "Settings", "Advanced"])
        bc.item_clicked.connect(print)
    """

    item_clicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items: list[str] = []
        self._labels: list[QLabel] = []
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

    def set_items(self, items: list[str]) -> None:
        """Set breadcrumb items."""
        # Clear
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._labels.clear()

        for i, text in enumerate(items):
            label = QLabel(text)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.mousePressEvent = lambda e, idx=i: self.item_clicked.emit(idx)
            self._labels.append(label)
            self._layout.addWidget(label)
            if i < len(items) - 1:
                sep = QLabel(" / ")
                sep.setStyleSheet(f"color: {tokens.NEUTRAL_400.name()};")
                self._layout.addWidget(sep)

        self._apply_style()

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _ui_css(dark)
        for i, label in enumerate(self._labels):
            if i == len(self._labels) - 1:
                label.setStyleSheet(f"font-weight: bold; color: {css['fg']};")
            else:
                label.setStyleSheet(f"color: {css['accent']}; text-decoration: underline;")


# ============================================================
# Steps
# ============================================================

class Steps(QWidget):
    """Vertical step indicator.

    Usage::

        steps = Steps()
        steps.set_steps(["Upload", "Process", "Done"])
        steps.set_current(1)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._steps: list[str] = []
        self._current = 0
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(spacing.XS)

    def set_steps(self, steps: list[str]) -> None:
        """Set step labels."""
        self._steps = steps
        self._build_ui()

    def set_current(self, index: int) -> None:
        """Set the current step index."""
        self._current = index
        self._build_ui()

    def _build_ui(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i, text in enumerate(self._steps):
            row = QHBoxLayout()
            row.setSpacing(spacing.SM)

            # Number circle
            circle = QLabel(str(i + 1))
            circle.setFixedSize(28, 28)
            circle.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Label
            label = QLabel(text)

            if i < self._current:
                circle.setStyleSheet(f"background-color: {tokens.SUCCESS.name()}; color: #ffffff; border-radius: 14px; font-size: 12px; font-weight: bold;")
                label.setStyleSheet(f"color: {tokens.SUCCESS.name()}; font-weight: bold;")
            elif i == self._current:
                circle.setStyleSheet(f"background-color: {tokens.PRIMARY_600.name()}; color: #ffffff; border-radius: 14px; font-size: 12px; font-weight: bold;")
                label.setStyleSheet(f"color: {tokens.PRIMARY_600.name()}; font-weight: bold;")
            else:
                circle.setStyleSheet(f"background-color: {tokens.NEUTRAL_200.name()}; color: {tokens.NEUTRAL_500.name()}; border-radius: 14px; font-size: 12px;")
                label.setStyleSheet(f"color: {tokens.NEUTRAL_500.name()};")

            row.addWidget(circle)
            row.addWidget(label)
            row.addStretch()

            container = QWidget()
            container.setLayout(row)
            self._layout.addWidget(container)


# ============================================================
# Badge
# ============================================================

class Badge(QLabel):
    """A small badge/counter label.

    Usage::

        badge = Badge("3")
        badge = Badge("New", variant="success")
    """

    def __init__(self, text: str = "", variant: str = "default", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(20)
        self._variant = variant
        self._apply_style()

    def _apply_style(self):
        colors = {
            "default": (tokens.NEUTRAL_100, tokens.NEUTRAL_700),
            "primary": (tokens.PRIMARY_100, tokens.PRIMARY_700),
            "success": (tokens.SUCCESS, "#ffffff"),
            "warning": (tokens.WARNING, "#ffffff"),
            "error": (tokens.ERROR, "#ffffff"),
        }
        bg, fg = colors.get(self._variant, colors["default"])
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg.name()};
                color: {fg.name() if hasattr(fg, 'name') else fg};
                border-radius: 10px;
                padding: 2px 8px;
                font-size: {typography.SM}px;
                font-weight: bold;
            }}
        """)


# ============================================================
# Alert
# ============================================================

class Alert(QFrame):
    """A styled alert/notification banner.

    Usage::

        alert = Alert("info", "This is an informational message.")
        alert = Alert("warning", "Something needs attention.")
        alert = Alert("error", "An error occurred.")
    """

    def __init__(self, variant: str = "info", text: str = "", parent=None):
        super().__init__(parent)
        self._variant = variant

        icon_map = {"info": "ℹ", "success": "✓", "warning": "⚠", "error": "✕"}
        color_map = {
            "info": (tokens.PRIMARY_50, tokens.PRIMARY_700, tokens.PRIMARY_200),
            "success": (QColor("#f0fdf4"), tokens.SUCCESS, QColor("#bbf7d0")),
            "warning": (QColor("#fffbeb"), tokens.WARNING, QColor("#fde68a")),
            "error": (QColor("#fef2f2"), tokens.ERROR, QColor("#fecaca")),
        }

        bg, fg, border = color_map.get(variant, color_map["info"])

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg.name()};
                color: {fg.name()};
                border: 1px solid {border.name()};
                border-radius: {spacing.SM}px;
                padding: {spacing.SM}px {spacing.MD}px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(spacing.SM, spacing.SM, spacing.SM, spacing.SM)
        layout.setSpacing(spacing.SM)

        icon = QLabel(icon_map.get(variant, "ℹ"))
        icon.setStyleSheet(f"font-size: {typography.LG}px; color: {fg.name()};")
        icon.setFixedWidth(20)

        self._label = QLabel(text)
        self._label.setStyleSheet(f"font-size: {typography.BASE}px; color: {fg.name()};")
        self._label.setWordWrap(True)

        layout.addWidget(icon)
        layout.addWidget(self._label, 1)

    def set_text(self, text: str) -> None:
        self._label.setText(text)


# ============================================================
# Timeline
# ============================================================

class Timeline(QWidget):
    """Vertical timeline with events.

    Usage::

        timeline = Timeline()
        timeline.add_event("Event 1", "Description 1")
        timeline.add_event("Event 2", "Description 2")
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._events: list[dict] = []

    def add_event(self, title: str, description: str = "", variant: str = "default") -> None:
        """Add a timeline event."""
        self._events.append({"title": title, "description": description, "variant": variant})
        self._rebuild()

    def clear_events(self):
        self._events.clear()
        self._rebuild()

    def _rebuild(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i, event in enumerate(self._events):
            container = QWidget()
            row = QHBoxLayout(container)
            row.setContentsMargins(0, 0, 0, spacing.SM)
            row.setSpacing(spacing.SM)

            # Dot
            dot = QLabel()
            dot.setFixedSize(12, 12)
            color_map = {
                "default": tokens.PRIMARY_600,
                "success": tokens.SUCCESS,
                "warning": tokens.WARNING,
                "error": tokens.ERROR,
            }
            color = color_map.get(event["variant"], tokens.PRIMARY_600)
            dot.setStyleSheet(f"background-color: {color.name()}; border-radius: 6px;")
            dot.setContentsMargins(0, 4, 0, 0)

            # Content
            content = QVBoxLayout()
            content.setSpacing(2)
            title = QLabel(event["title"])
            title.setStyleSheet(f"font-weight: bold; font-size: {typography.SM}px;")
            content.addWidget(title)
            if event["description"]:
                desc = QLabel(event["description"])
                desc.setStyleSheet(f"color: {tokens.NEUTRAL_500.name()}; font-size: {typography.SM}px;")
                desc.setWordWrap(True)
                content.addWidget(desc)

            row.addWidget(dot)
            row.addLayout(content, 1)
            self._layout.addWidget(container)

        self._layout.addStretch()


# ============================================================
# TransferList
# ============================================================

class TransferList(QWidget):
    """Dual list for moving items between two groups.

    Usage::

        transfer = TransferList()
        transfer.set_source_items(["A", "B", "C"])
        transfer.set_target_items(["D", "E"])
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing.SM)

        # Source
        src_col = QVBoxLayout()
        src_col.addWidget(QLabel("Available"))
        self._source = QListWidget()
        self._source.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        src_col.addWidget(self._source)

        # Buttons
        btn_col = QVBoxLayout()
        btn_col.addStretch()
        self._btn_right = QPushButton("→")
        self._btn_right.setFixedSize(32, 32)
        self._btn_right.clicked.connect(self._move_right)
        self._btn_left = QPushButton("←")
        self._btn_left.setFixedSize(32, 32)
        self._btn_left.clicked.connect(self._move_left)
        btn_col.addWidget(self._btn_right)
        btn_col.addWidget(self._btn_left)
        btn_col.addStretch()

        # Target
        tgt_col = QVBoxLayout()
        tgt_col.addWidget(QLabel("Selected"))
        self._target = QListWidget()
        self._target.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        tgt_col.addWidget(self._target)

        layout.addLayout(src_col, 2)
        layout.addLayout(btn_col)
        layout.addLayout(tgt_col, 2)

        self._apply_style()

    def set_source_items(self, items: list[str]) -> None:
        self._source.clear()
        self._source.addItems(items)

    def set_target_items(self, items: list[str]) -> None:
        self._target.clear()
        self._target.addItems(items)

    def source_items(self) -> list[str]:
        return [self._source.item(i).text() for i in range(self._source.count())]

    def target_items(self) -> list[str]:
        return [self._target.item(i).text() for i in range(self._target.count())]

    def _move_right(self):
        for item in self._source.selectedItems():
            self._target.addItem(item.text())
            self._source.takeItem(self._source.row(item))

    def _move_left(self):
        for item in self._target.selectedItems():
            self._source.addItem(item.text())
            self._target.takeItem(self._target.row(item))

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _ui_css(dark)
        list_css = f"""
            QListWidget {{
                background-color: {css['bg']};
                color: {css['fg']};
                border: 1px solid {css['border']};
                border-radius: {css['radius']}px;
                padding: {css['pad']}px;
                font-size: {css['font_size']}px;
            }}
            QListWidget::item {{
                padding: 4px 8px;
                border-radius: 3px;
            }}
            QListWidget::item:selected {{
                background-color: {css['accent_bg']};
            }}
        """
        btn_css = f"""
            QPushButton {{
                background-color: {css['accent']};
                color: #ffffff;
                border: none;
                border-radius: {css['radius']}px;
                font-size: {css['font_size']}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """
        self._source.setStyleSheet(list_css)
        self._target.setStyleSheet(list_css)
        self._btn_right.setStyleSheet(btn_css)
        self._btn_left.setStyleSheet(btn_css)
