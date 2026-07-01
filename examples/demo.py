"""Minimal demo — styled buttons, inputs, and toast notifications."""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFormLayout,
)
from PySide6.QtCore import Qt

# Add src to path for local dev
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.theme import ThemeManager, PlotTheme
from pyqtcomponents.widgets import (
    StyledButton, Toast,
    StyledInput, StyledSpinBox, StyledDoubleSpinBox, StyledComboBox,
    StyledCheckBox, StyledRadioButton, StyledSearchComboBox,
    StyledMultiSelectComboBox,
    StyledGroupBox, StyledCard, StyledDivider,
)
from pyqtcomponents.icons import IconProvider


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtComponents Demo")
        self.setMinimumSize(700, 550)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Title
        title = QLabel("PyQtComponents Demo")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Buttons section
        section = QLabel("Buttons")
        section.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(section)

        for level in ("primary", "secondary", "tertiary", "danger"):
            row = QHBoxLayout()
            row.setSpacing(8)
            for size in ("compact", "standard", "loose"):
                btn = StyledButton(f"{level.title()} {size.title()}", level=level, size=size)
                row.addWidget(btn)
            layout.addLayout(row)

        # Inputs section
        section2 = QLabel("Input Controls")
        section2.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(section2)

        form = QFormLayout()
        form.setSpacing(8)

        form.addRow("Text Input:", StyledInput("Enter text..."))
        form.addRow("Error Input:", StyledInput("Invalid value"))
        form.addRow("Spin Box:", StyledSpinBox())
        form.addRow("Double Spin:", StyledDoubleSpinBox())

        combo = StyledComboBox()
        combo.addItems(["Option A", "Option B", "Option C"])
        form.addRow("ComboBox:", combo)

        search_combo = StyledSearchComboBox()
        search_combo.addItems([
            "Apple", "Banana", "Cherry", "Date", "Elderberry",
            "Fig", "Grape", "Honeydew", "Kiwi", "Lemon",
        ])
        form.addRow("Search Select:", search_combo)

        multi_select = StyledMultiSelectComboBox()
        multi_select.addItems(["Red", "Green", "Blue", "Yellow", "Purple"])
        form.addRow("Multi-Select:", multi_select)

        layout.addLayout(form)

        # Checkboxes & Radios section
        section3 = QLabel("Checkboxes & Radio Buttons")
        section3.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(section3)

        check_row = QHBoxLayout()
        check_row.setSpacing(16)
        check_row.addWidget(StyledCheckBox("Option 1"))
        c2 = StyledCheckBox("Option 2")
        c2.setChecked(True)
        check_row.addWidget(c2)
        c3 = StyledCheckBox("Disabled")
        c3.setEnabled(False)
        check_row.addWidget(c3)
        check_row.addStretch()
        layout.addLayout(check_row)

        radio_row = QHBoxLayout()
        radio_row.setSpacing(16)
        radio_row.addWidget(StyledRadioButton("Choice A"))
        r2 = StyledRadioButton("Choice B")
        r2.setChecked(True)
        radio_row.addWidget(r2)
        r3 = StyledRadioButton("Disabled")
        r3.setEnabled(False)
        radio_row.addWidget(r3)
        radio_row.addStretch()
        layout.addLayout(radio_row)

        # Panels section
        section4 = QLabel("Panels & Cards")
        section4.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(section4)

        layout.addWidget(StyledDivider())

        card_row = QHBoxLayout()
        card_row.setSpacing(12)

        card1 = StyledCard()
        card1_layout = QVBoxLayout(card1)
        card1_layout.addWidget(QLabel("Card 1"))
        card1_layout.addWidget(QLabel("Content here"))
        card_row.addWidget(card1)

        card2 = StyledCard()
        card2_layout = QVBoxLayout(card2)
        card2_layout.addWidget(QLabel("Card 2"))
        card2_layout.addWidget(QLabel("More content"))
        card_row.addWidget(card2)

        layout.addLayout(card_row)

        layout.addWidget(StyledDivider())

        # Plot colors section
        section5 = QLabel("Plot Data Colors (Colorblind-friendly)")
        section5.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(section5)

        plot_theme = PlotTheme()
        plot_cfg = plot_theme.light()

        color_row = QHBoxLayout()
        color_row.setSpacing(8)
        for i, color in enumerate(plot_cfg.data_colors):
            swatch = QLabel()
            swatch.setFixedSize(32, 32)
            swatch.setStyleSheet(f"background-color: {color.name()}; border-radius: 4px;")
            color_row.addWidget(swatch)
        color_row.addStretch()
        layout.addLayout(color_row)

        layout.addWidget(StyledDivider())

        layout.addStretch()

        # Icons section
        section6 = QLabel("Icons (SVG)")
        section6.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(section6)

        icons = IconProvider()
        icon_row = QHBoxLayout()
        icon_row.setSpacing(12)
        for name in ["file", "folder", "search", "settings", "check", "close"]:
            for size in ["sm", "md", "lg"]:
                lbl = QLabel()
                pixmap = icons.get_pixmap(name, size=size)
                lbl.setPixmap(pixmap)
                lbl.setToolTip(f"{name} ({size})")
                icon_row.addWidget(lbl)
        icon_row.addStretch()
        layout.addLayout(icon_row)

        # Toast trigger
        toast_btn = StyledButton("Show Toast", level="primary", size="loose")
        toast_btn.clicked.connect(lambda: Toast.show("Action completed!", parent=self))
        layout.addWidget(toast_btn, alignment=Qt.AlignmentFlag.AlignLeft)


def main():
    app = QApplication(sys.argv)
    theme = ThemeManager(mode="light")
    theme.apply(app)
    win = DemoWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
