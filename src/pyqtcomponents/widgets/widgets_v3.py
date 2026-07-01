"""Widgets v3 — Tag, SegmentedControl, StatCard, EmptyState, SkeletonLoader,
Rate, TreeView, BackToTop, Watermark."""

from PySide6.QtCore import Qt, Signal, QTimer, QRect
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTreeWidget, QTreeWidgetItem, QScrollArea,
    QApplication,
)

from ..theme import tokens, spacing, typography


def _css(dark: bool) -> dict:
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
        "skeleton": tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_700.name(),
        "skeleton_shine": tokens.NEUTRAL_100.name() if not dark else tokens.NEUTRAL_600.name(),
        "radius": 4,
        "pad": spacing.SM,
        "font_size": typography.BASE,
        "font_sm": typography.SM,
        "font_lg": typography.LG,
        "font_xl": typography.XL,
        "font_xxl": typography.XXL,
    }


# ============================================================
# Tag
# ============================================================

class Tag(QFrame):
    """An interactive tag/chip with optional close button.

    Usage::

        tag = Tag("Python")
        tag = Tag("React", closable=True)
        tag.closed.connect(lambda: tag.deleteLater())
    """

    closed = Signal()

    def __init__(self, text: str = "", closable: bool = False, variant: str = "default", parent=None):
        super().__init__(parent)
        self._variant = variant
        self.setFrameShape(QFrame.Shape.NoFrame)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(spacing.SM, spacing.XS, spacing.SM, spacing.XS)
        layout.setSpacing(spacing.XS)

        self._label = QLabel(text)
        layout.addWidget(self._label)

        if closable:
            close_btn = QPushButton("×")
            close_btn.setFixedSize(16, 16)
            close_btn.setStyleSheet("border: none; font-weight: bold;")
            close_btn.clicked.connect(self.closed.emit)
            layout.addWidget(close_btn)

        self._apply_style()

    def text(self) -> str:
        return self._label.text()

    def _apply_style(self):
        colors = {
            "default": (tokens.NEUTRAL_100, tokens.NEUTRAL_700),
            "primary": (tokens.PRIMARY_100, tokens.PRIMARY_700),
            "success": (QColor("#dcfce7"), tokens.SUCCESS),
            "warning": (QColor("#fef3c7"), tokens.WARNING),
            "error": (QColor("#fee2e2"), tokens.ERROR),
        }
        bg, fg = colors.get(self._variant, colors["default"])
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg.name()};
                border-radius: {spacing.SM}px;
            }}
            QLabel {{
                color: {fg.name()};
                font-size: {typography.SM}px;
            }}
        """)


# ============================================================
# SegmentedControl
# ============================================================

class SegmentedControl(QWidget):
    """A segmented control / pill selector.

    Usage::

        seg = SegmentedControl(["Day", "Week", "Month"])
        seg.current_changed.connect(print)
    """

    current_changed = Signal(int)

    def __init__(self, options: list[str] = None, parent=None):
        super().__init__(parent)
        self._options = options or []
        self._current = 0
        self._buttons: list[QPushButton] = []

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._build()
        self._apply_style()

    def set_options(self, options: list[str]):
        self._options = options
        self._build()

    def current_index(self) -> int:
        return self._current

    def _build(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._buttons.clear()

        for i, text in enumerate(self._options):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setChecked(i == self._current)
            btn.clicked.connect(lambda checked, idx=i: self._on_click(idx))
            self._buttons.append(btn)
            self._layout.addWidget(btn)

    def _on_click(self, index: int):
        self._current = index
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i == index)
        self.current_changed.emit(index)

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _css(dark)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {css['fg']};
                border: none;
                padding: {css['pad']}px {spacing.MD}px;
                font-size: {css['font_size']}px;
                border-radius: {css['radius']}px;
            }}
            QPushButton:hover {{
                background-color: {css['bg_hover']};
            }}
            QPushButton:checked {{
                background-color: {css['accent']};
                color: #ffffff;
                font-weight: bold;
            }}
        """)


# ============================================================
# StatCard
# ============================================================

class StatCard(QFrame):
    """A statistic display card.

    Usage::

        card = StatCard("Total Users", "12,345", "+12% from last month")
    """

    def __init__(self, title: str = "", value: str = "", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(spacing.MD, spacing.MD, spacing.MD, spacing.MD)
        layout.setSpacing(spacing.XS)

        self._title = QLabel(title)
        self._title.setStyleSheet(f"font-size: {typography.SM}px;")
        layout.addWidget(self._title)

        self._value = QLabel(value)
        self._value.setStyleSheet(f"font-size: {typography.XXL}px; font-weight: bold;")
        layout.addWidget(self._value)

        if subtitle:
            self._subtitle = QLabel(subtitle)
            self._subtitle.setStyleSheet(f"font-size: {typography.SM}px;")
            layout.addWidget(self._subtitle)

        layout.addStretch()
        self._apply_style()

    def set_value(self, value: str):
        self._value.setText(value)

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _css(dark)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {css['bg']};
                border: 1px solid {css['border']};
                border-radius: {spacing.MD}px;
            }}
            QLabel {{
                color: {css['fg']};
            }}
        """)


# ============================================================
# EmptyState
# ============================================================

class EmptyState(QWidget):
    """An empty state placeholder.

    Usage::

        empty = EmptyState("No data", "Import a file to get started.")
    """

    def __init__(self, title: str = "No data", description: str = "", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(spacing.SM)

        self._icon = QLabel("📭")
        self._icon.setStyleSheet(f"font-size: 48px;")
        self._icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._icon)

        self._title = QLabel(title)
        self._title.setStyleSheet(f"font-size: {typography.LG}px; font-weight: bold;")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._title)

        if description:
            self._desc = QLabel(description)
            self._desc.setStyleSheet(f"color: {tokens.NEUTRAL_500.name()};")
            self._desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._desc.setWordWrap(True)
            layout.addWidget(self._desc)


# ============================================================
# SkeletonLoader
# ============================================================

class SkeletonLoader(QWidget):
    """A skeleton loading placeholder with animated shimmer.

    Usage::

        skeleton = SkeletonLoader(lines=3)
    """

    def __init__(self, lines: int = 3, parent=None):
        super().__init__(parent)
        self._lines = lines
        self._offset = 0

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(50)

        self.setMinimumHeight(lines * 32)

    def _animate(self):
        self._offset = (self._offset + 2) % 100
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        base_color = QColor(tokens.NEUTRAL_200 if not dark else tokens.NEUTRAL_700)
        shine_color = QColor(tokens.NEUTRAL_100 if not dark else tokens.NEUTRAL_600)

        for i in range(self._lines):
            y = i * 36 + 8
            width = self.width() - (i % 3) * 40 - 20
            if width < 60:
                width = 60

            # Base bar
            painter.setBrush(QBrush(base_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(0, y, width, 20, 4, 4)

            # Shine effect
            shine_x = int((self._offset / 100) * width)
            painter.setBrush(QBrush(shine_color))
            painter.drawRoundedRect(shine_x - 20, y, 40, 20, 4, 4)

        painter.end()

    def stop(self):
        self._timer.stop()

    def start(self):
        self._timer.start(50)


# ============================================================
# Rate
# ============================================================

class Rate(QWidget):
    """Star rating widget.

    Usage::

        rate = Rate(max_stars=5)
        rate.rating_changed.connect(print)
    """

    rating_changed = Signal(int)

    def __init__(self, max_stars: int = 5, rating: int = 0, parent=None):
        super().__init__(parent)
        self._max = max_stars
        self._rating = rating
        self._hover = 0

        self.setMouseTracking(True)
        self.setFixedSize(max_stars * 28, 28)

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int):
        self._rating = max(0, min(self._max, value))
        self.update()
        self.rating_changed.emit(self._rating)

    def mouseMoveEvent(self, event):
        x = event.position().x()
        self._hover = int(x / 28) + 1
        self.update()

    def leaveEvent(self, event):
        self._hover = 0
        self.update()

    def mousePressEvent(self, event):
        x = event.position().x()
        self._rating = int(x / 28) + 1
        self.update()
        self.rating_changed.emit(self._rating)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False

        for i in range(self._max):
            x = i * 28
            if i < self._rating:
                color = QColor(tokens.WARNING)  # filled star
            elif i < self._hover:
                color = QColor(tokens.WARNING).lighter(130)  # hover star
            else:
                color = QColor(tokens.NEUTRAL_300 if not dark else tokens.NEUTRAL_600)

            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            # Simple star shape using text
            painter.setFont(QFont("Arial", 16))
            painter.setPen(QPen(color))
            painter.drawText(QRect(x, 0, 28, 28), Qt.AlignmentFlag.AlignCenter, "★")

        painter.end()


# ============================================================
# TreeView
# ============================================================

class TreeView(QTreeWidget):
    """A themed tree view.

    Usage::

        tree = TreeView()
        tree.setHeaderLabels(["Name", "Type"])
        parent = QTreeWidgetItem(tree, ["Folder", "dir"])
        QTreeWidgetItem(parent, ["File 1", "file"])
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self._apply_style()

    def _apply_style(self):
        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False
        css = _css(dark)
        self.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {css['bg']};
                color: {css['fg']};
                border: 1px solid {css['border']};
                border-radius: {css['radius']}px;
                font-size: {css['font_size']}px;
            }}
            QTreeWidget::item {{
                padding: {css['pad']}px;
            }}
            QTreeWidget::item:selected {{
                background-color: {css['accent_bg']};
            }}
            QHeaderView::section {{
                background-color: {tokens.NEUTRAL_100 if not dark else tokens.NEUTRAL_700};
                border: none;
                border-bottom: 1px solid {css['border']};
                padding: {css['pad']}px;
                font-weight: bold;
            }}
        """)


# ============================================================
# BackToTop
# ============================================================

class BackToTop(QWidget):
    """A floating back-to-top button.

    Usage::

        btt = BackToTop(scroll_area=my_scroll)
        layout.addWidget(btt)
    """

    clicked = Signal()

    def __init__(self, scroll_area: QScrollArea = None, parent=None):
        super().__init__(parent)
        self._scroll = scroll_area
        self.setFixedSize(40, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hide()

        if scroll_area:
            scroll_area.verticalScrollBar().valueChanged.connect(self._check_visibility)

    def _check_visibility(self, value):
        if self._scroll:
            max_val = self._scroll.verticalScrollBar().maximum()
            self.setVisible(value > max_val * 0.3)

    def mousePressEvent(self, event):
        if self._scroll:
            self._scroll.verticalScrollBar().setValue(0)
        self.clicked.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False

        # Circle background
        painter.setBrush(QBrush(QColor(tokens.PRIMARY_600 if not dark else tokens.PRIMARY_400)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 40, 40)

        # Arrow
        painter.setPen(QPen(QColor("#ffffff"), 2))
        painter.drawLine(12, 22, 20, 14)
        painter.drawLine(20, 14, 28, 22)
        painter.end()


# ============================================================
# Watermark
# ============================================================

class Watermark(QWidget):
    """A watermark overlay for content.

    Usage::

        watermark = Watermark("CONFIDENTIAL")
        parent_layout.addWidget(watermark)
    """

    def __init__(self, text: str = "WATERMARK", parent=None):
        super().__init__(parent)
        self._text = text
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setStyleSheet("background: transparent;")

    def set_text(self, text: str):
        self._text = text
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        app = QApplication.instance()
        dark = app.palette().window().color().lightness() < 128 if app else False

        color = QColor(tokens.NEUTRAL_200 if not dark else tokens.NEUTRAL_700)
        color.setAlpha(40)

        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QPen(color))

        # Draw rotated text across the widget
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(-30)
        painter.drawText(QRect(-200, -30, 400, 60), Qt.AlignmentFlag.AlignCenter, self._text)
        painter.end()
