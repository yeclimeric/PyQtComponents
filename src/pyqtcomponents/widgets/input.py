"""Styled input controls — QLineEdit, QSpinBox, QComboBox, QCheckBox, QRadioButton."""

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSortFilterProxyModel
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QLineEdit, QSpinBox, QComboBox, QDoubleSpinBox,
    QCheckBox, QRadioButton, QListWidget, QListWidgetItem,
    QVBoxLayout, QApplication, QWidget,
)

from ..theme import tokens, spacing, typography


# ---------------------------------------------------------------------------
# Shared QSS for all input controls
# ---------------------------------------------------------------------------
_INPUT_QSS = """
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: {bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: {pad_v}px {pad_h}px;
    font-size: {font_size}px;
    min-height: {height}px;
    selection-background-color: {selection};
}}
QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {{
    border: 1px solid {border_hover};
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border: 1px solid {border_focus};
    outline: none;
}}
QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled {{
    background-color: {bg_disabled};
    color: {fg_disabled};
    border: 1px solid {border_disabled};
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 24px;
    border: none;
}}
QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
}}
QComboBox QAbstractItemView {{
    background-color: {bg};
    color: {fg};
    border: 1px solid {border};
    selection-background-color: {selection};
    selection-color: {fg};
    padding: 4px;
}}
"""

_RADIUS = 4
_HEIGHT = 32
_PAD_V = spacing.SM
_PAD_H = spacing.SM + spacing.XS  # 12px


def _input_css(dark: bool) -> str:
    """Build the QSS string for the current theme mode."""
    return _INPUT_QSS.format(
        bg="#ffffff" if not dark else tokens.NEUTRAL_800.name(),
        fg=tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
        border=tokens.NEUTRAL_300.name() if not dark else tokens.NEUTRAL_600.name(),
        border_hover=tokens.NEUTRAL_400.name() if not dark else tokens.NEUTRAL_500.name(),
        border_focus=tokens.PRIMARY_500.name() if not dark else tokens.PRIMARY_400.name(),
        bg_disabled=tokens.NEUTRAL_100.name() if not dark else tokens.NEUTRAL_700.name(),
        fg_disabled=tokens.NEUTRAL_400.name() if not dark else tokens.NEUTRAL_500.name(),
        border_disabled=tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_700.name(),
        selection=tokens.PRIMARY_200.name() if not dark else tokens.PRIMARY_800.name(),
        radius=_RADIUS,
        font_size=typography.BASE,
        height=_HEIGHT,
        pad_v=_PAD_V,
        pad_h=_PAD_H,
    )


def _apply_input_style(widget: QWidget) -> None:
    """Apply theme-aware QSS to an input widget."""
    app = QApplication.instance()
    dark = False
    if app is not None:
        dark = app.palette().window().color().lightness() < 128
    widget.setStyleSheet(_input_css(dark))


class StyledInput(QLineEdit):
    """A themed single-line text input.

    Supports an optional ``error`` state that highlights the border in red.
    """

    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self._error = False
        self._apply_style()

    @property
    def error(self) -> bool:
        return self._error

    @error.setter
    def error(self, value: bool) -> None:
        self._error = value
        self._apply_style()

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128

        css = _input_css(dark)
        if self._error:
            error_border = f"border: 1px solid {tokens.ERROR.name()};"
            # Inject error border into the base state rules
            css = css.replace(
                "border: 1px solid {border};",
                f"border: 1px solid {tokens.ERROR.name()};",
            )
        self.setStyleSheet(css)


class StyledSpinBox(QSpinBox):
    """A themed integer spin box."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()

    def _apply_style(self) -> None:
        _apply_input_style(self)


class StyledDoubleSpinBox(QDoubleSpinBox):
    """A themed floating-point spin box."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()

    def _apply_style(self) -> None:
        _apply_input_style(self)


class StyledComboBox(QComboBox):
    """A themed drop-down combo box."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()

    def _apply_style(self) -> None:
        _apply_input_style(self)


# ---------------------------------------------------------------------------
# Checkbox and Radio — QSS with custom indicator indicators
# ---------------------------------------------------------------------------

_CHECK_QSS = """
QCheckBox {{
    color: {fg};
    font-size: {font_size}px;
    spacing: {spacing}px;
}}
QCheckBox:disabled {{
    color: {fg_disabled};
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 2px solid {border};
    border-radius: {check_radius}px;
    background-color: {bg};
}}
QCheckBox::indicator:hover {{
    border-color: {border_hover};
}}
QCheckBox::indicator:checked {{
    background-color: {accent};
    border-color: {accent};
}}
QCheckBox::indicator:disabled {{
    border-color: {border_disabled};
    background-color: {bg_disabled};
}}
"""

_RADIO_QSS = """
QRadioButton {{
    color: {fg};
    font-size: {font_size}px;
    spacing: {spacing}px;
}}
QRadioButton:disabled {{
    color: {fg_disabled};
}}
QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border: 2px solid {border};
    border-radius: 9px;
    background-color: {bg};
}}
QRadioButton::indicator:hover {{
    border-color: {border_hover};
}}
QRadioButton::indicator:checked {{
    background-color: {bg};
    border-color: {accent};
    border-width: 5px;
}}
QRadioButton::indicator:disabled {{
    border-color: {border_disabled};
    background-color: {bg_disabled};
}}
"""


def _toggle_css(dark: bool) -> dict:
    """Shared color dict for checkbox/radio QSS."""
    return {
        "bg": "#ffffff" if not dark else tokens.NEUTRAL_800.name(),
        "fg": tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
        "fg_disabled": tokens.NEUTRAL_400.name() if not dark else tokens.NEUTRAL_500.name(),
        "border": tokens.NEUTRAL_400.name() if not dark else tokens.NEUTRAL_500.name(),
        "border_hover": tokens.NEUTRAL_500.name() if not dark else tokens.NEUTRAL_400.name(),
        "border_disabled": tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_600.name(),
        "accent": tokens.PRIMARY_600.name() if not dark else tokens.PRIMARY_400.name(),
        "font_size": typography.BASE,
        "spacing": spacing.SM,
        "check_radius": 3,
        "bg_disabled": tokens.NEUTRAL_100.name() if not dark else tokens.NEUTRAL_700.name(),
    }


def _apply_toggle_style(widget: QWidget, qss_template: str) -> None:
    """Apply theme-aware QSS to a checkbox or radio widget."""
    app = QApplication.instance()
    dark = False
    if app is not None:
        dark = app.palette().window().color().lightness() < 128
    widget.setStyleSheet(qss_template.format(**_toggle_css(dark)))


class StyledCheckBox(QCheckBox):
    """A themed checkbox with a 16×16 rounded indicator."""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self._apply_style()

    def _apply_style(self) -> None:
        _apply_toggle_style(self, _CHECK_QSS)


class StyledRadioButton(QRadioButton):
    """A themed radio button with a 16×16 circular indicator."""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self._apply_style()

    def _apply_style(self) -> None:
        _apply_toggle_style(self, _RADIO_QSS)


# ---------------------------------------------------------------------------
# Searchable ComboBox — filter-as-you-type
# ---------------------------------------------------------------------------

class StyledSearchComboBox(QComboBox):
    """A themed combo box with filter-as-you-type search.

    As the user types in the edit field, the dropdown filters to show
    only items that contain the typed text (case-insensitive).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.setDuplicatesEnabled(False)

        # Proxy model for filtering
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._proxy.setFilterKeyColumn(0)

        # Store source items and build model on demand
        self._items: list[str] = []

        # Connect text changes to filter
        self.lineEdit().textChanged.connect(self._on_text_changed)
        self.currentIndexChanged.connect(self._on_index_changed)

        self._apply_style()

    def addItems(self, texts) -> None:
        """Add items to the searchable list."""
        self._items.extend(texts)
        self._rebuild_model()

    def clear(self) -> None:
        """Clear all items."""
        self._items.clear()
        self._rebuild_model()

    def _rebuild_model(self) -> None:
        """Rebuild the model from stored items, applying current filter."""
        from PySide6.QtGui import QStandardItemModel, QStandardItem
        model = QStandardItemModel()
        for item in self._items:
            model.appendRow(QStandardItem(item))
        self._proxy.setSourceModel(model)
        super().setModel(self._proxy)

    def _on_text_changed(self, text: str) -> None:
        """Filter the dropdown based on the current text."""
        self._proxy.setFilterFixedString(text)
        if text and self._proxy.rowCount() > 0:
            self.showPopup()

    def _on_index_changed(self, index: int) -> None:
        """Clear the filter when an item is selected."""
        if index >= 0:
            self.lineEdit().clear()
            self._proxy.setFilterFixedString("")

    def _apply_style(self) -> None:
        _apply_input_style(self)


# ---------------------------------------------------------------------------
# Multi-Select ComboBox — checkboxes with tag display and search
# ---------------------------------------------------------------------------

_MULTI_SELECT_QSS = """
QLineEdit {{
    background-color: {bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: {pad_v}px {pad_h}px;
    font-size: {font_size}px;
    min-height: {height}px;
}}
QLineEdit:hover {{
    border: 1px solid {border_hover};
}}
QLineEdit:focus {{
    border: 1px solid {border_focus};
}}
QLineEdit:disabled {{
    background-color: {bg_disabled};
    color: {fg_disabled};
    border: 1px solid {border_disabled};
}}
QListWidget {{
    background-color: {bg};
    color: {fg};
    border: none;
    border-radius: 0 0 {radius}px {radius}px;
    padding: 4px;
    font-size: {font_size}px;
}}
QListWidget::item {{
    padding: 6px 8px;
    border-radius: 3px;
}}
QListWidget::item:hover {{
    background-color: {bg_hover};
}}
QListWidget::item:selected {{
    background-color: {selection};
}}
"""

_POPUP_QSS = """
QWidget {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: {radius}px;
}}
"""


class _SearchInput(QLineEdit):
    """QLineEdit that moves focus to list on Down arrow."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._on_down_pressed = None  # callback

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Down:
            if self._on_down_pressed:
                self._on_down_pressed()
        else:
            super().keyPressEvent(event)


class _KeyboardListWidget(QListWidget):
    """QListWidget with keyboard shortcuts for multi-select."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._on_escape = None  # callback
        self._on_space = None   # callback

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self._on_escape:
                self._on_escape()
        elif event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self._on_space:
                self._on_space()
        else:
            super().keyPressEvent(event)


class StyledMultiSelectComboBox(QWidget):
    """A multi-select combo box with checkboxes, tag display, and search filter.

    Shows a text input with selected items displayed as comma-separated text.
    Clicking opens a popup with a search input and checkboxes for each item.
    Typing in the search filters the list in real time.

    Keyboard navigation:
    - Arrow Up/Down: move focus through items
    - Space/Enter: toggle checkbox on focused item
    - Escape: close popup
    - Down arrow in search field: move focus to list
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items: list[str] = []
        self._selected: set[str] = set()

        # Main line edit (read-only, shows selection)
        self._line = QLineEdit(self)
        self._line.setReadOnly(True)
        self._line.setPlaceholderText("Select items...")
        self._line.mousePressEvent = self._toggle_popup
        self._line.keyPressEvent = self._line_key_press

        # Popup container
        self._popup = QWidget(self)
        self._popup.setWindowFlags(Qt.WindowType.Popup)

        popup_layout = QVBoxLayout(self._popup)
        popup_layout.setContentsMargins(0, 0, 0, 0)
        popup_layout.setSpacing(0)

        # Search input inside popup
        self._search = _SearchInput(self._popup)
        self._search.setPlaceholderText("Search...")
        self._search.textChanged.connect(self._filter_items)
        self._search._on_down_pressed = self._focus_list

        # Select all / Deselect all buttons
        from PySide6.QtWidgets import QHBoxLayout, QPushButton
        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(spacing.SM, spacing.XS, spacing.SM, spacing.XS)
        self._btn_select_all = QPushButton("Select All", self._popup)
        self._btn_deselect_all = QPushButton("Deselect All", self._popup)
        self._btn_select_all.clicked.connect(self._select_all)
        self._btn_deselect_all.clicked.connect(self._deselect_all)
        btn_row.addWidget(self._btn_select_all)
        btn_row.addWidget(self._btn_deselect_all)
        btn_row.addStretch()

        # List widget with keyboard handling
        self._list = _KeyboardListWidget(self._popup)
        self._list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self._list.itemChanged.connect(self._on_item_changed)
        self._list._on_escape = self._close_popup
        self._list._on_space = self._toggle_current

        popup_layout.addWidget(self._search)
        popup_layout.addLayout(btn_row)
        popup_layout.addWidget(self._list)

        self._apply_style()

    def addItems(self, texts) -> None:
        """Add items to the multi-select list."""
        for text in texts:
            self._items.append(text)
            item = QListWidgetItem(text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self._list.addItem(item)

    def clear(self) -> None:
        """Clear all items and selections."""
        self._items.clear()
        self._selected.clear()
        self._list.clear()
        self._line.clear()
        self._search.clear()

    def selectedItems(self) -> list[str]:
        """Return list of selected item texts."""
        return sorted(self._selected)

    def setSelectedItems(self, texts: list[str]) -> None:
        """Set selected items by text."""
        self._selected = set(texts)
        for i in range(self._list.count()):
            item = self._list.item(i)
            item.setCheckState(
                Qt.CheckState.Checked if item.text() in self._selected
                else Qt.CheckState.Unchecked
            )
        self._update_display()

    def _toggle_popup(self, event=None) -> None:
        """Show or hide the popup."""
        if self._popup.isVisible():
            self._popup.hide()
        else:
            self._search.clear()
            self._filter_items("")
            # Position below the line edit
            pos = self._line.mapToGlobal(self._line.rect().bottomLeft())
            self._popup.move(pos)
            self._popup.setFixedWidth(self._line.width())
            self._popup.show()
            self._search.setFocus()

    def _line_key_press(self, event) -> None:
        """Handle key press on the main line edit."""
        if event.key() == Qt.Key.Key_Down:
            self._toggle_popup()
        else:
            QLineEdit.keyPressEvent(self._line, event)

    def _focus_list(self) -> None:
        """Move focus from search input to the list."""
        if self._list.count() > 0:
            # Find first visible item
            for i in range(self._list.count()):
                if not self._list.item(i).isHidden():
                    self._list.setCurrentRow(i)
                    self._list.setFocus()
                    break

    def _close_popup(self) -> None:
        """Close the popup."""
        self._popup.hide()
        self._line.setFocus()

    def _toggle_current(self) -> None:
        """Toggle the checkbox on the currently focused list item."""
        item = self._list.currentItem()
        if item:
            new_state = (
                Qt.CheckState.Unchecked
                if item.checkState() == Qt.CheckState.Checked
                else Qt.CheckState.Checked
            )
            item.setCheckState(new_state)

    def _filter_items(self, text: str) -> None:
        """Show/hide items based on search text."""
        text_lower = text.lower()
        for i in range(self._list.count()):
            item = self._list.item(i)
            item.setHidden(text_lower not in item.text().lower())

    def _select_all(self) -> None:
        """Select all visible (non-hidden) items."""
        for i in range(self._list.count()):
            item = self._list.item(i)
            if not item.isHidden():
                item.setCheckState(Qt.CheckState.Checked)

    def _deselect_all(self) -> None:
        """Deselect all items."""
        for i in range(self._list.count()):
            self._list.item(i).setCheckState(Qt.CheckState.Unchecked)

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        """Handle checkbox toggle."""
        if item.checkState() == Qt.CheckState.Checked:
            self._selected.add(item.text())
        else:
            self._selected.discard(item.text())
        self._update_display()

    def _update_display(self) -> None:
        """Update the line edit text with selected items."""
        if self._selected:
            self._line.setText(", ".join(sorted(self._selected)))
        else:
            self._line.clear()

    def _apply_style(self) -> None:
        app = QApplication.instance()
        dark = False
        if app is not None:
            dark = app.palette().window().color().lightness() < 128

        css = _MULTI_SELECT_QSS.format(
            bg="#ffffff" if not dark else tokens.NEUTRAL_800.name(),
            fg=tokens.NEUTRAL_900.name() if not dark else tokens.NEUTRAL_50.name(),
            border=tokens.NEUTRAL_300.name() if not dark else tokens.NEUTRAL_600.name(),
            border_hover=tokens.NEUTRAL_400.name() if not dark else tokens.NEUTRAL_500.name(),
            border_focus=tokens.PRIMARY_500.name() if not dark else tokens.PRIMARY_400.name(),
            bg_disabled=tokens.NEUTRAL_100.name() if not dark else tokens.NEUTRAL_700.name(),
            fg_disabled=tokens.NEUTRAL_400.name() if not dark else tokens.NEUTRAL_500.name(),
            border_disabled=tokens.NEUTRAL_200.name() if not dark else tokens.NEUTRAL_600.name(),
            bg_hover=tokens.NEUTRAL_50.name() if not dark else tokens.NEUTRAL_700.name(),
            selection=tokens.PRIMARY_200.name() if not dark else tokens.PRIMARY_800.name(),
            radius=_RADIUS,
            font_size=typography.BASE,
            height=_HEIGHT,
            pad_v=_PAD_V,
            pad_h=_PAD_H,
        )
        self._line.setStyleSheet(css)
        # Search input uses same styling but smaller min-height
        self._search.setStyleSheet(css.replace("min-height: 32px", "min-height: 28px"))
        self._list.setStyleSheet(css)

        popup_css = _POPUP_QSS.format(
            bg="#ffffff" if not dark else tokens.NEUTRAL_800.name(),
            border=tokens.NEUTRAL_300.name() if not dark else tokens.NEUTRAL_600.name(),
            radius=_RADIUS,
        )
        self._popup.setStyleSheet(popup_css)
