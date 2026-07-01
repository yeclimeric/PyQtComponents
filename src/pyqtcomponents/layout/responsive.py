"""Responsive three-panel layout with auto-folding.

Per spec D11:
- Main window: min 1024px, default screen 70%
- Left panel: min 200px, default 280px
- Central panel: min 500px, elastic
- Right panel: min 180px, default 240px
- Width < 900px: right panel folds to icon bar
- Width < 700px: left panel folds to icon bar
- State saved to QSettings
"""

from PySide6.QtCore import Qt, QSettings, QSize
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QPushButton, QToolButton, QApplication,
)

from ..theme import tokens, spacing


# ---------------------------------------------------------------------------
# Fold thresholds (px)
# ---------------------------------------------------------------------------
FOLD_RIGHT = 900
FOLD_LEFT = 700

# ---------------------------------------------------------------------------
# Default sizes (px)
# ---------------------------------------------------------------------------
LEFT_DEFAULT = 280
LEFT_MIN = 200
RIGHT_DEFAULT = 240
RIGHT_MIN = 180
CENTER_MIN = 500

SETTINGS_ORG = "PyQtComponents"
SETTINGS_APP = "ResponsiveLayout"


class ResponsiveLayout(QWidget):
    """A three-panel layout that auto-folds side panels into icon bars.

    Usage::

        layout = ResponsiveLayout()
        layout.set_left_content(my_left_widget)
        layout.set_center_content(my_center_widget)
        layout.set_right_content(my_right_widget)

    The layout monitors its width and folds side panels when the window
    gets too narrow. Fold state is persisted via QSettings.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings = QSettings(SETTINGS_ORG, SETTINGS_APP)

        # State
        self._left_folded = False
        self._right_folded = False

        # Icon bar buttons (hidden when expanded)
        self._left_toggle = QToolButton(self)
        self._left_toggle.setText("\u2630")  # hamburger
        self._left_toggle.setCheckable(True)
        self._left_toggle.setFixedWidth(36)
        self._left_toggle.clicked.connect(self._toggle_left)

        self._right_toggle = QToolButton(self)
        self._right_toggle.setText("\u2699")  # gear
        self._right_toggle.setCheckable(True)
        self._right_toggle.setFixedWidth(36)
        self._right_toggle.clicked.connect(self._toggle_right)

        # Panels
        self._left_panel = QWidget()
        self._left_panel.setMinimumWidth(LEFT_MIN)
        self._left_panel.setMaximumWidth(LEFT_DEFAULT)

        self._center_panel = QWidget()
        self._center_panel.setMinimumWidth(CENTER_MIN)

        self._right_panel = QWidget()
        self._right_panel.setMinimumWidth(RIGHT_MIN)
        self._right_panel.setMaximumWidth(RIGHT_DEFAULT)

        # Main splitter
        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.addWidget(self._left_panel)
        self._splitter.addWidget(self._center_panel)
        self._splitter.addWidget(self._right_panel)
        self._splitter.setStretchFactor(0, 0)
        self._splitter.setStretchFactor(1, 1)
        self._splitter.setStretchFactor(2, 0)

        # Layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self._left_toggle)
        main_layout.addWidget(self._splitter)
        main_layout.addWidget(self._right_toggle)

        # Restore saved state
        self._restore_state()

    # -- public API -----------------------------------------------------------

    def set_left_content(self, widget: QWidget) -> None:
        """Set the content of the left panel."""
        self._set_panel_content(self._left_panel, widget)

    def set_center_content(self, widget: QWidget) -> None:
        """Set the content of the center panel."""
        self._set_panel_content(self._center_panel, widget)

    def set_right_content(self, widget: QWidget) -> None:
        """Set the content of the right panel."""
        self._set_panel_content(self._right_panel, widget)

    @property
    def is_left_folded(self) -> bool:
        return self._left_folded

    @property
    def is_right_folded(self) -> bool:
        return self._right_folded

    # -- internal -------------------------------------------------------------

    def _set_panel_content(self, panel: QWidget, widget: QWidget) -> None:
        """Replace the content of a panel."""
        layout = panel.layout()
        if layout is None:
            layout = QVBoxLayout(panel)
            layout.setContentsMargins(0, 0, 0, 0)
        else:
            # Clear existing
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
        layout.addWidget(widget)

    def _toggle_left(self) -> None:
        """Toggle left panel fold state."""
        self._left_folded = not self._left_folded
        self._apply_fold()
        self._save_state()

    def _toggle_right(self) -> None:
        """Toggle right panel fold state."""
        self._right_folded = not self._right_folded
        self._apply_fold()
        self._save_state()

    def _apply_fold(self) -> None:
        """Apply fold state to panels."""
        self._left_panel.setVisible(not self._left_folded)
        self._right_panel.setVisible(not self._right_folded)
        self._left_toggle.setChecked(self._left_folded)
        self._right_toggle.setChecked(self._right_folded)

    def _save_state(self) -> None:
        """Persist fold state to QSettings."""
        self._settings.setValue("left_folded", self._left_folded)
        self._settings.setValue("right_folded", self._right_folded)

    def _restore_state(self) -> None:
        """Restore fold state from QSettings."""
        self._left_folded = self._settings.value("left_folded", False, type=bool)
        self._right_folded = self._settings.value("right_folded", False, type=bool)
        self._apply_fold()

    def resizeEvent(self, event) -> None:
        """Auto-fold panels based on window width."""
        super().resizeEvent(event)
        w = event.size().width()
        # Auto-fold right panel
        if w < FOLD_RIGHT and not self._right_folded:
            self._right_folded = True
            self._apply_fold()
        # Auto-fold left panel
        if w < FOLD_LEFT and not self._left_folded:
            self._left_folded = True
            self._apply_fold()
        # Auto-expand when enough space
        if w >= FOLD_RIGHT and self._right_folded:
            self._right_folded = False
            self._apply_fold()
        if w >= FOLD_LEFT and self._left_folded:
            self._left_folded = False
            self._apply_fold()
        self._save_state()
