"""Synaptipy — Electrophysiology Data Visualization Application

Main application integrating all PyQtComponents.
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFormLayout, QSplitter, QTextEdit,
)
from PySide6.QtCore import Qt

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.theme import ThemeManager, PlotTheme
from pyqtcomponents.widgets import (
    StyledButton, Toast,
    StyledInput, StyledSpinBox, StyledDoubleSpinBox, StyledComboBox,
    StyledCheckBox, StyledRadioButton, StyledSearchComboBox,
    StyledMultiSelectComboBox,
    StyledGroupBox, StyledCard, StyledDivider,
    StyledProgressBar, StyledSlider, StyledTabWidget,
    StyledMessageBox, StyledInputDialog,
)
from pyqtcomponents.icons import IconProvider
from pyqtcomponents.layout import ResponsiveLayout


class MainWindow(QMainWindow):
    """Main application window with three-panel layout."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Synaptipy — Electrophysiology Viewer")
        self.setMinimumSize(1024, 700)

        # Icons
        self.icons = IconProvider()

        # Main responsive layout
        layout = ResponsiveLayout()
        layout.set_left_content(self._build_left_panel())
        layout.set_center_content(self._build_center_panel())
        layout.set_right_content(self._build_right_panel())
        self.setCentralWidget(layout)

    def _build_left_panel(self) -> QWidget:
        """Build the left panel — file browser and filters."""
        panel = QWidget()
        vbox = QVBoxLayout(panel)
        vbox.setContentsMargins(12, 12, 12, 12)
        vbox.setSpacing(12)

        # File section
        file_group = StyledGroupBox("Files")
        file_layout = QVBoxLayout()

        search = StyledSearchComboBox()
        search.addItems([
            "session_001.npy", "session_002.npy", "session_003.npy",
            "recording_a.dat", "recording_b.dat", "stimulus.pkl",
        ])
        file_layout.addWidget(QLabel("Search files:"))
        file_layout.addWidget(search)

        multi = StyledMultiSelectComboBox()
        multi.addItems(["Spike sorted", "Raw LFP", "Behavior", "Stimulus"])
        file_layout.addWidget(QLabel("Data types:"))
        file_layout.addWidget(multi)

        file_group.setLayout(file_layout)
        vbox.addWidget(file_group)

        # Filters section
        filter_group = StyledGroupBox("Filters")
        filter_layout = QFormLayout()

        filter_layout.addRow("Channel:", StyledSpinBox())
        filter_layout.addRow("Min freq:", StyledDoubleSpinBox())
        filter_layout.addRow("Max freq:", StyledDoubleSpinBox())

        filter_group.setLayout(filter_layout)
        vbox.addWidget(filter_group)

        # Actions
        load_btn = StyledButton("Load Data", level="primary", size="standard")
        load_btn.setIcon(self.icons.get("file", size="sm"))
        load_btn.clicked.connect(self._on_load)
        vbox.addWidget(load_btn)

        clear_btn = StyledButton("Clear", level="secondary", size="standard")
        clear_btn.setIcon(self.icons.get("close", size="sm"))
        clear_btn.clicked.connect(self._on_clear)
        vbox.addWidget(clear_btn)

        vbox.addStretch()
        return panel

    def _build_center_panel(self) -> QWidget:
        """Build the center panel — visualization area."""
        panel = QWidget()
        vbox = QVBoxLayout(panel)
        vbox.setContentsMargins(12, 12, 12, 12)
        vbox.setSpacing(12)

        # Status bar
        status_row = QHBoxLayout()
        status_row.addWidget(QLabel("Ready"))
        status_row.addStretch()

        progress = StyledProgressBar()
        progress.setRange(0, 100)
        progress.setValue(0)
        progress.setFixedWidth(200)
        self._progress = progress
        status_row.addWidget(progress)
        vbox.addLayout(status_row)

        # Tabs for different views
        tabs = StyledTabWidget()

        # Waveform tab
        waveform_tab = QWidget()
        waveform_layout = QVBoxLayout(waveform_tab)
        waveform_layout.addWidget(QLabel("Waveform visualization area"))
        waveform_layout.addWidget(QLabel("(Matplotlib canvas would go here)"))
        tabs.addTab(waveform_tab, "Waveforms")

        # Raster tab
        raster_tab = QWidget()
        raster_layout = QVBoxLayout(raster_tab)
        raster_layout.addWidget(QLabel("Raster plot area"))
        tabs.addTab(raster_tab, "Raster")

        # ISI tab
        isi_tab = QWidget()
        isi_layout = QVBoxLayout(isi_tab)
        isi_layout.addWidget(QLabel("ISI histogram area"))
        tabs.addTab(isi_tab, "ISI")

        vbox.addWidget(tabs)

        # Playback controls
        play_row = QHBoxLayout()
        play_row.setSpacing(8)

        play_btn = StyledButton("Play", level="primary", size="compact")
        play_btn.setIcon(self.icons.get("check", size="sm"))
        play_btn.clicked.connect(self._on_play)
        play_row.addWidget(play_btn)

        speed_slider = StyledSlider()
        speed_slider.setRange(1, 10)
        speed_slider.setValue(5)
        play_row.addWidget(QLabel("Speed:"))
        play_row.addWidget(speed_slider)

        play_row.addStretch()
        vbox.addLayout(play_row)

        return panel

    def _build_right_panel(self) -> QWidget:
        """Build the right panel — properties and settings."""
        panel = QWidget()
        vbox = QVBoxLayout(panel)
        vbox.setContentsMargins(12, 12, 12, 12)
        vbox.setSpacing(12)

        # Properties card
        props_card = StyledCard()
        props_layout = QVBoxLayout(props_card)
        props_layout.addWidget(QLabel("Properties"))

        props_form = QFormLayout()
        props_form.addRow("Channels:", QLabel("32"))
        props_form.addRow("Duration:", QLabel("60.5s"))
        props_form.addRow("Sampling:", QLabel("30 kHz"))
        props_form.addRow("Units:", QLabel("12"))
        props_layout.addLayout(props_form)
        vbox.addWidget(props_card)

        StyledDivider()

        # Settings section
        settings_group = StyledGroupBox("Display")
        settings_layout = QVBoxLayout()

        settings_layout.addWidget(StyledCheckBox("Show grid"))
        settings_layout.addWidget(StyledCheckBox("Color by unit"))
        c = StyledCheckBox("Auto-scale")
        c.setChecked(True)
        settings_layout.addWidget(c)

        color_label = QLabel("Line color:")
        settings_layout.addWidget(color_label)
        settings_layout.addWidget(StyledComboBox())

        settings_group.setLayout(settings_layout)
        vbox.addWidget(settings_group)

        # Contrast check
        contrast_card = StyledCard()
        contrast_layout = QVBoxLayout(contrast_card)
        contrast_layout.addWidget(QLabel("Accessibility"))
        from pyqtcomponents.theme.contrast import ContrastReport
        from PySide6.QtGui import QColor
        report = ContrastReport(QColor("#111827"), QColor("#ffffff"))
        ratio_label = QLabel(f"Contrast: {report.ratio:.1f}:1")
        contrast_layout.addWidget(ratio_label)
        vbox.addWidget(contrast_card)

        vbox.addStretch()

        # Export button
        export_btn = StyledButton("Export", level="secondary", size="standard")
        export_btn.setIcon(self.icons.get("settings", size="sm"))
        export_btn.clicked.connect(self._on_export)
        vbox.addWidget(export_btn)

        return panel

    def _on_load(self):
        """Handle load button click."""
        self._progress.setValue(0)
        Toast.show("Loading data...", parent=self)

    def _on_clear(self):
        """Handle clear button click."""
        if StyledMessageBox.question("Confirm", "Clear all loaded data?", self):
            self._progress.setValue(0)
            Toast.show("Data cleared", parent=self)

    def _on_play(self):
        """Handle play button click."""
        Toast.show("Playback started", parent=self)

    def _on_export(self):
        """Handle export button click."""
        Toast.show("Export started", parent=self)


def main():
    app = QApplication(sys.argv)

    # Apply theme
    theme = ThemeManager(mode="light")
    theme.apply(app)

    # Apply focus styles
    from pyqtcomponents.theme.focus import apply_focus_style
    apply_focus_style(app)

    # Show window
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
