"""Extra widgets — Cascader, Switch, CollapsiblePanel, Drawer, NavigationBar, TabPagination."""

from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QScrollArea, QStackedWidget, QApplication,
)

from ..theme import tokens, spacing, typography


# ---------------------------------------------------------------------------
# Shared QSS
# ---------------------------------------------------------------------------

_SWITCH_QSS = """
Switch {{
    background-color: {track_off};
    border-radius: {radius}px;
    min-width: {width}px;
    min-height: {height}px;
}}
Switch::indicator {{
    background-color: {thumb};
    border-radius: {thumb_radius}px;
    width: {thumb_size}px;
    height: {thumb_size}px;
    margin: {margin}px;
}}
Switch::indicator:checked {{
    background-color: {accent};
}}
"""

_COLLAPSIBLE_QSS = """
QFrame#collapsible_header {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: {pad}px;
}}
QFrame#collapsible_header:hover {{
    background-color: {bg_hover};
}}
"""

_DRAWER_QSS = """
QWidget#drawer {{
    background-color: {bg};
    border-left: 1px solid {border};
}}
"""

_NAV_QSS = """
QWidget#navbar {{
    background-color: {bg};
    border-bottom: 1px solid {border};
}}
QPushButton {{
    background-color: transparent;
    color: {fg};
    border: none;
    border-radius: {radius}px;
    padding: {pad}px {pad_h}px;
    font-size: {font_size}px;
    text-align: left;
}}
QPushButton:hover {{
    background-color: {bg_hover};
}}
QPushButton:checked {{
    background-color: {bg_active};
    color: {accent};
    font-weight: bold;
}}
"""

_PAGINATION_QSS = """
QPushButton {{
    background-color: {bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: {pad}px;
    min-width: 32px;
    font-size: {font_size}px;
}}
QPushButton:hover {{
    background-color: {bg_hover};
}}
QPushButton:checked {{
    background-color: {accent};
    color: #ffffff;
    border-color: {accent};
}}
QPushButton:disabled {{
    color: {fg_disabled};
}}
"""


def _extra_css(dark: bool) -> dict:
    return {
        "bg": "#ffffff" if not dark else tokens.NEUTRAL_800.name(),
        "fg": tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
        "fg_disabled": tokens.NEUTRAL_400.name() if not dark else tokens.NEUTRAL_500.name(),
        "border": tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_600.name(),
        "bg_hover": tokens.NEUTRAL_50.name() if not dark else tokens.NEUTRAL_700.name(),
        "bg_active": tokens.PRIMARY_50.name() if not dark else tokens.PRIMARY_900.name(),
        "accent": tokens.PRIMARY_600.name() if not dark else tokens.PRIMARY_400.name(),
        "track_off": tokens.NEUTRAL_300.name() if not dark else tokens.NEUTRAL_600.name(),
        "thumb": "#ffffff",
        "thumb_size": 20,
        "thumb_radius": 10,
        "margin": 2,
        "width": 44,
        "height": 24,
        "radius": 12,
        "pad": spacing.SM,
        "pad_h": spacing.MD,
        "font_size": typography.BASE,
    }


# ============================================================
# Cascader
# ============================================================

class Cascader(QWidget):
    """Cascading select — click to drill into nested options.

    Usage::

        cascader = Cascader()
        cascader.set_options({
            "Fruits": {"Apple": "apple", "Banana": "banana"},
            "Vegetables": {"Carrot": "carrot", "Pea": "pea"},
        })
        cascader.value_changed.connect(print)
    """

    value_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._options: dict[str, dict[str, str]] = {}
        self._path: list[str] = []
        self._result: str = ""

        self._line = QLineEdit(self)
        self._line.setReadOnly(True)
        self._line.setPlaceholderText("Select...")
        self._line.mousePressEvent = lambda e: self._toggle()

        self._popup = QListWidget(self)
        self._popup.hide()
        self._popup.itemClicked.connect(self._on_click)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._line)
        layout.addWidget(self._popup)

        self._apply_style()

    def set_options(self, options: dict[str, dict[str, str]]) -> None:
        """Set options as {category: {label: value}}."""
        self._options = options
        self._show_categories()

    @property
    def value(self) -> str:
        return self._result

    def _toggle(self):
        if self._popup.isVisible():
            self._popup.hide()
        else:
            self._path.clear()
            self._show_categories()
            self._popup.setFixedWidth(self._line.width())
            self._popup.show()
            self._popup.raise_()

    def _show_categories(self):
        self._popup.clear()
        self._popup.addItem("← Back" if self._path else "Select...")
        for cat in self._options:
            self._popup.addItem(cat)

    def _show_items(self, category: str):
        self._popup.clear()
        self._popup.addItem("← Back")
        for label in self._options[category]:
            self._popup.addItem(label)

    def _on_click(self, item: QListWidgetItem):
        text = item.text()
        if text == "← Back":
            if self._path:
                self._path.pop()
                self._show_categories()
            else:
                self._popup.hide()
            return
        if text == "Select...":
            self._popup.hide()
            return

        if not self._path:
            self._path.append(text)
            self._show_items(text)
        else:
            cat = self._path[0]
            val = self._options[cat].get(text, text)
            self._result = val
            self._line.setText(f"{cat} / {text}")
            self._popup.hide()
            self.value_changed.emit(val)

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _extra_css(dark)
        self._line.setStyleSheet(f"""
            QLineEdit {{
                background-color: {css['bg']};
                color: {css['fg']};
                border: 1px solid {css['border']};
                border-radius: {css['radius']}px;
                padding: {css['pad']}px;
                font-size: {css['font_size']}px;
                min-height: 32px;
            }}
        """)
        self._popup.setStyleSheet(f"""
            QListWidget {{
                background-color: {css['bg']};
                color: {css['fg']};
                border: 1px solid {css['border']};
                border-radius: {css['radius']}px;
                padding: {css['pad']}px;
                font-size: {css['font_size']}px;
            }}
            QListWidget::item {{
                padding: 6px 8px;
                border-radius: 3px;
            }}
            QListWidget::item:hover {{
                background-color: {css['bg_hover']};
            }}
        """)


# ============================================================
# Switch
# ============================================================

class StyledSwitch(QWidget):
    """A toggle switch with on/off state.

    Usage::

        switch = StyledSwitch()
        switch.toggled.connect(print)
    """

    toggled = Signal(bool)

    def __init__(self, checked: bool = False, parent=None):
        super().__init__(parent)
        self._checked = checked
        self.setFixedSize(44, 24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    @property
    def checked(self) -> bool:
        return self._checked

    @checked.setter
    def checked(self, value: bool):
        self._checked = value
        self.update()
        self.toggled.emit(value)

    def toggle(self):
        self.checked = not self._checked

    def mousePressEvent(self, event):
        self.toggle()

    def paintEvent(self, event):
        from PySide6.QtGui import QPainter, QBrush
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Track
        track_color = QColor(tokens.PRIMARY_600 if self._checked else (tokens.NEUTRAL_600 if dark else tokens.NEUTRAL_300))
        painter.setBrush(QBrush(track_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 44, 24, 12, 12)

        # Thumb
        thumb_x = 24 if self._checked else 4
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.drawEllipse(thumb_x, 2, 20, 20)
        painter.end()


# ============================================================
# CollapsiblePanel
# ============================================================

class CollapsiblePanel(QWidget):
    """A collapsible panel with header and content.

    Usage::

        panel = CollapsiblePanel("Section Title")
        panel.set_content(QLabel("Content here"))
    """

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._expanded = True

        # Header
        self._header = QFrame()
        self._header.setObjectName("collapsible_header")
        self._header.setCursor(Qt.CursorShape.PointingHandCursor)
        self._header.mousePressEvent = lambda e: self.toggle()

        header_layout = QHBoxLayout(self._header)
        header_layout.setContentsMargins(spacing.SM, spacing.SM, spacing.SM, spacing.SM)
        self._arrow = QLabel("▼")
        self._arrow.setFixedWidth(16)
        self._title_label = QLabel(title)
        self._title_label.setStyleSheet(f"font-weight: bold; font-size: {typography.SM}px;")
        header_layout.addWidget(self._arrow)
        header_layout.addWidget(self._title_label)
        header_layout.addStretch()

        # Content
        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(spacing.LG, spacing.SM, spacing.LG, spacing.SM)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._header)
        layout.addWidget(self._content)

        self._apply_style()

    def set_content(self, widget: QWidget) -> None:
        """Set the content widget."""
        self._content_layout.addWidget(widget)

    def add_content(self, widget: QWidget) -> None:
        """Add a widget to the content area."""
        self._content_layout.addWidget(widget)

    def toggle(self):
        """Toggle expand/collapse."""
        self._expanded = not self._expanded
        self._content.setVisible(self._expanded)
        self._arrow.setText("▼" if self._expanded else "▶")

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _extra_css(dark)
        self._header.setStyleSheet(f"""
            QFrame#collapsible_header {{
                background-color: {css['bg']};
                border: 1px solid {css['border']};
                border-radius: {css['radius']}px;
            }}
            QFrame#collapsible_header:hover {{
                background-color: {css['bg_hover']};
            }}
        """)


# ============================================================
# Drawer
# ============================================================

class Drawer(QWidget):
    """A slide-in drawer panel from the right side.

    Usage::

        drawer = Drawer(parent=main_window)
        drawer.set_content(QLabel("Drawer content"))
        drawer.open()
    """

    def __init__(self, width: int = 300, parent=None):
        super().__init__(parent)
        self._width = width
        self._open = False

        self.setObjectName("drawer")
        self.setFixedWidth(width)
        self.hide()

        self._content = QWidget(self)
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(spacing.LG, spacing.LG, spacing.LG, spacing.LG)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._content)

        self._apply_style()

    def set_content(self, widget: QWidget) -> None:
        """Set the drawer content."""
        self._content_layout.addWidget(widget)

    def open(self):
        """Show the drawer."""
        if self.parent():
            parent_width = self.parent().width()
            self.setGeometry(parent_width - self._width, 0, self._width, self.parent().height())
        self.show()
        self.raise_()
        self._open = True

    def close(self):
        """Hide the drawer."""
        self.hide()
        self._open = False

    def toggle(self):
        if self._open:
            self.close()
        else:
            self.open()

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _extra_css(dark)
        self.setStyleSheet(f"""
            QWidget#drawer {{
                background-color: {css['bg']};
                border-left: 1px solid {css['border']};
            }}
        """)


# ============================================================
# NavigationBar
# ============================================================

class NavigationBar(QWidget):
    """A vertical navigation bar with icon buttons.

    Usage::

        nav = NavigationBar()
        nav.add_item("home", "Home")
        nav.add_item("settings", "Settings")
        nav.current_changed.connect(print)
    """

    current_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("navbar")
        self._buttons: list[QPushButton] = []
        self._current = -1

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(spacing.SM, spacing.SM, spacing.SM, spacing.SM)
        self._layout.setSpacing(spacing.XS)
        self._layout.addStretch()

        self._apply_style()

    def add_item(self, icon_name: str, label: str) -> QPushButton:
        """Add a navigation item."""
        btn = QPushButton(f"  {label}", self)
        btn.setCheckable(True)
        btn.clicked.connect(lambda checked, idx=len(self._buttons): self._on_click(idx))
        self._buttons.append(btn)
        # Insert before the stretch
        self._layout.insertWidget(self._layout.count() - 1, btn)
        if self._current == -1:
            btn.setChecked(True)
            self._current = 0
        return btn

    def current_index(self) -> int:
        return self._current

    def _on_click(self, index: int):
        if self._current >= 0 and self._current < len(self._buttons):
            self._buttons[self._current].setChecked(False)
        self._current = index
        self._buttons[index].setChecked(True)
        self.current_changed.emit(index)

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _extra_css(dark)
        self.setStyleSheet(f"""
            QWidget#navbar {{
                background-color: {css['bg']};
                border-right: 1px solid {css['border']};
            }}
            QPushButton {{
                background-color: transparent;
                color: {css['fg']};
                border: none;
                border-radius: {css['radius']}px;
                padding: {css['pad']}px {css['pad_h']}px;
                font-size: {css['font_size']}px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {css['bg_hover']};
            }}
            QPushButton:checked {{
                background-color: {css['bg_active']};
                color: {css['accent']};
                font-weight: bold;
            }}
        """)


# ============================================================
# TabPagination
# ============================================================

class TabPagination(QWidget):
    """A horizontal pagination bar with page buttons.

    Usage::

        pag = TabPagination(total_pages=10)
        pag.page_changed.connect(print)
    """

    page_changed = Signal(int)

    def __init__(self, total_pages: int = 1, parent=None):
        super().__init__(parent)
        self._total = total_pages
        self._current = 0
        self._buttons: list[QPushButton] = []

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(spacing.XS)

        self._build_buttons()
        self._apply_style()

    def set_total_pages(self, total: int):
        """Update total pages."""
        self._total = total
        self._build_buttons()

    def current_page(self) -> int:
        return self._current

    def _build_buttons(self):
        # Clear old buttons
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._buttons.clear()

        for i in range(self._total):
            btn = QPushButton(str(i + 1))
            btn.setCheckable(True)
            btn.setFixedSize(32, 32)
            btn.clicked.connect(lambda checked, idx=i: self._on_click(idx))
            self._buttons.append(btn)
            self._layout.addWidget(btn)

        if self._buttons:
            self._buttons[0].setChecked(True)

    def _on_click(self, index: int):
        if self._current < len(self._buttons):
            self._buttons[self._current].setChecked(False)
        self._current = index
        self._buttons[index].setChecked(True)
        self.page_changed.emit(index)

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _extra_css(dark)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {css['bg']};
                color: {css['fg']};
                border: 1px solid {css['border']};
                border-radius: {css['radius']}px;
                padding: {css['pad']}px;
                min-width: 32px;
                font-size: {css['font_size']}px;
            }}
            QPushButton:hover {{
                background-color: {css['bg_hover']};
            }}
            QPushButton:checked {{
                background-color: {css['accent']};
                color: #ffffff;
                border-color: {css['accent']};
            }}
        """)
