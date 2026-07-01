"""Screen reader and accessibility support.

Per spec D12:
- Icon buttons have aria-label
- Group boxes have label association
- Dynamic content has live region
- Tables have header association
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGroupBox, QPushButton, QTableWidget


def set_accessible_name(widget: QWidget, name: str) -> None:
    """Set the accessible name for screen readers.

    This is the Qt equivalent of aria-label.
    """
    widget.setAccessibleName(name)


def set_accessible_description(widget: QWidget, description: str) -> None:
    """Set the accessible description for screen readers.

    This is the Qt equivalent of aria-description.
    """
    widget.setAccessibleDescription(description)


def set_accessible_properties(
    widget: QWidget,
    name: str | None = None,
    description: str | None = None,
    role: str | None = None,
) -> None:
    """Set multiple accessibility properties at once.

    Args:
        widget: Target widget
        name: Accessible name (aria-label equivalent)
        description: Accessible description
        role: Accessible role (for custom widgets)
    """
    if name is not None:
        widget.setAccessibleName(name)
    if description is not None:
        widget.setAccessibleDescription(description)
    if role is not None:
        widget.setAccessibleRole(role)


class AccessibleGroup(QGroupBox):
    """A group box with proper label association for screen readers.

    Per spec: group boxes must have label association.
    """

    def __init__(self, title: str = "", parent=None):
        super().__init__(title, parent)
        self.setAccessibleName(title)
        self.setAccessibleDescription(f"Group: {title}")


class AccessibleButton(QPushButton):
    """A button with accessible name and optional shortcut hint.

    Per spec: icon buttons must have aria-label.
    """

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        if text:
            self.setAccessibleName(text)

    def set_shortcut_hint(self, shortcut: str) -> None:
        """Set a keyboard shortcut hint for screen readers."""
        current_desc = self.accessibleDescription()
        hint = f"Shortcut: {shortcut}"
        self.setAccessibleDescription(f"{current_desc} {hint}".strip())


class AccessibleTable(QTableWidget):
    """A table with proper header association for screen readers.

    Per spec: tables must have header association.
    """

    def __init__(self, rows: int = 0, columns: int = 0, parent=None):
        super().__init__(rows, columns, parent)
        self._update_accessible()

    def setHorizontalHeaderLabels(self, labels: list[str]) -> None:
        """Set horizontal headers with accessibility support."""
        super().setHorizontalHeaderLabels(labels)
        self._update_accessible()

    def _update_accessible(self) -> None:
        """Update accessibility info based on table contents."""
        rows = self.rowCount()
        cols = self.columnCount()
        headers = []
        for c in range(cols):
            item = self.horizontalHeaderItem(c)
            if item:
                headers.append(item.text())
        desc = f"Table with {rows} rows and {cols} columns"
        if headers:
            desc += f". Columns: {', '.join(headers)}"
        self.setAccessibleDescription(desc)
