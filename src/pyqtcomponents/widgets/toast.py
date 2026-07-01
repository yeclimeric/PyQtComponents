"""Toast — lightweight fire-and-forget notification."""

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QLabel, QFrame, QWidget, QGraphicsOpacityEffect, QApplication

from ..theme import spacing, typography


class _ToastWidget(QFrame):
    """Internal frameless toast window."""

    _QSS = """
    QFrame {{
        background-color: #1f2937;
        color: #ffffff;
        border-radius: 8px;
        padding: {pad_v}px {pad_h}px;
    }}
    """

    def __init__(self, message: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(self._QSS.format(
            pad_v=spacing.MD, pad_h=spacing.LG,
        ))

        label = QLabel(message, self)
        label.setStyleSheet(f"font-size: {typography.BASE}px; background: transparent;")
        pal = label.palette()
        pal.setColor(QPalette.WindowText, QColor("#ffffff"))
        pal.setColor(QPalette.Text, QColor("#ffffff"))
        label.setPalette(pal)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Fade in/out via opacity effect
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)

        self.adjustSize()

    def _fade_in(self) -> None:
        anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        anim.setDuration(200)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.start()
        # prevent GC
        self._anim = anim

    def _fade_out(self, on_done) -> None:
        anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        anim.setDuration(200)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.finished.connect(on_done)
        anim.start()
        self._anim = anim

    def _position(self, parent: QWidget) -> None:
        """Center horizontally, 24px from bottom of *parent*."""
        pw = parent.width() if parent else 400
        ph = parent.height() if parent else 300
        tw = self.width()
        x = (pw - tw) // 2
        y = ph - self.height() - spacing.XL
        self.move(x, y)


class Toast:
    """Fire-and-forget toast notification."""

    @staticmethod
    def show(
        message: str,
        duration: int = 3000,
        parent: QWidget | None = None,
    ) -> None:
        """Display a toast at the bottom-center of *parent*.

        The toast auto-dismisses after *duration* ms with a fade-out animation.
        """
        if parent is None:
            parent = QApplication.activeWindow()
        if parent is None:
            return

        toast = _ToastWidget(message, parent)
        toast._position(parent)
        toast.show()
        toast._fade_in()

        QTimer.singleShot(duration, lambda: toast._fade_out(toast.close))
