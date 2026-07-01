"""Smoke tests for styled input controls."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.widgets.input import (
    StyledInput, StyledSpinBox, StyledDoubleSpinBox, StyledComboBox,
    StyledCheckBox, StyledRadioButton, StyledSearchComboBox,
    StyledMultiSelectComboBox,
)


# ---------- StyledInput ----------

def test_input_instantiate(qtbot):
    w = StyledInput("placeholder")
    qtbot.addWidget(w)
    assert w.placeholderText() == "placeholder"


def test_input_set_text(qtbot):
    w = StyledInput()
    qtbot.addWidget(w)
    w.setText("hello")
    assert w.text() == "hello"


def test_input_error_state(qtbot):
    w = StyledInput()
    qtbot.addWidget(w)
    assert not w.error
    w.error = True
    assert w.error
    w.error = False
    assert not w.error


# ---------- StyledSpinBox ----------

def test_spinbox_instantiate(qtbot):
    w = StyledSpinBox()
    qtbot.addWidget(w)
    assert w.value() == 0


def test_spinbox_set_value(qtbot):
    w = StyledSpinBox()
    qtbot.addWidget(w)
    w.setValue(42)
    assert w.value() == 42


def test_spinbox_range(qtbot):
    w = StyledSpinBox()
    qtbot.addWidget(w)
    w.setRange(0, 100)
    w.setValue(200)
    assert w.value() == 100


# ---------- StyledDoubleSpinBox ----------

def test_double_spinbox_instantiate(qtbot):
    w = StyledDoubleSpinBox()
    qtbot.addWidget(w)
    assert w.value() == 0.0


def test_double_spinbox_set_value(qtbot):
    w = StyledDoubleSpinBox()
    qtbot.addWidget(w)
    w.setValue(3.14)
    assert abs(w.value() - 3.14) < 0.001


# ---------- StyledComboBox ----------

def test_combobox_instantiate(qtbot):
    w = StyledComboBox()
    qtbot.addWidget(w)
    assert w.count() == 0


def test_combobox_add_items(qtbot):
    w = StyledComboBox()
    qtbot.addWidget(w)
    w.addItems(["A", "B", "C"])
    assert w.count() == 3
    assert w.currentText() == "A"


def test_combobox_select(qtbot):
    w = StyledComboBox()
    qtbot.addWidget(w)
    w.addItems(["X", "Y", "Z"])
    w.setCurrentIndex(2)
    assert w.currentText() == "Z"


# ---------- StyledCheckBox ----------

def test_checkbox_instantiate(qtbot):
    w = StyledCheckBox("Check me")
    qtbot.addWidget(w)
    assert w.text() == "Check me"
    assert not w.isChecked()


def test_checkbox_toggle(qtbot):
    w = StyledCheckBox("Toggle")
    qtbot.addWidget(w)
    w.setChecked(True)
    assert w.isChecked()
    w.setChecked(False)
    assert not w.isChecked()


def test_checkbox_disabled(qtbot):
    w = StyledCheckBox("Disabled")
    qtbot.addWidget(w)
    w.setEnabled(False)
    assert not w.isEnabled()


# ---------- StyledRadioButton ----------

def test_radio_instantiate(qtbot):
    w = StyledRadioButton("Radio me")
    qtbot.addWidget(w)
    assert w.text() == "Radio me"
    assert not w.isChecked()


def test_radio_select(qtbot):
    w = StyledRadioButton("Select")
    qtbot.addWidget(w)
    w.setChecked(True)
    assert w.isChecked()


def test_radio_disabled(qtbot):
    w = StyledRadioButton("Disabled")
    qtbot.addWidget(w)
    w.setEnabled(False)
    assert not w.isEnabled()


# ---------- StyledSearchComboBox ----------

def test_search_combo_instantiate(qtbot):
    w = StyledSearchComboBox()
    qtbot.addWidget(w)
    assert w.isEditable()


def test_search_combo_add_items(qtbot):
    w = StyledSearchComboBox()
    qtbot.addWidget(w)
    w.addItems(["Alpha", "Beta", "Gamma"])
    assert w.count() == 3


def test_search_combo_filter(qtbot):
    w = StyledSearchComboBox()
    qtbot.addWidget(w)
    w.addItems(["Apple", "Banana", "Cherry"])
    # Type to filter
    w.lineEdit().setText("app")
    qtbot.wait(50)
    # Should filter down to items containing "app" (case-insensitive)
    visible = [w.model().index(i, 0).data() for i in range(w.model().rowCount())]
    assert "Apple" in visible


def test_search_combo_select(qtbot):
    w = StyledSearchComboBox()
    qtbot.addWidget(w)
    w.addItems(["X", "Y", "Z"])
    w.setCurrentIndex(1)
    # For editable combos, currentText() reflects the edit field;
    # check the model data at the current index instead
    idx = w.currentIndex()
    assert idx == 1
    assert w.model().index(idx, 0).data() == "Y"


# ---------- StyledMultiSelectComboBox ----------

def test_multi_select_instantiate(qtbot):
    w = StyledMultiSelectComboBox()
    qtbot.addWidget(w)
    assert w.selectedItems() == []


def test_multi_select_add_items(qtbot):
    w = StyledMultiSelectComboBox()
    qtbot.addWidget(w)
    w.addItems(["A", "B", "C"])
    assert w._list.count() == 3


def test_multi_select_set_selected(qtbot):
    w = StyledMultiSelectComboBox()
    qtbot.addWidget(w)
    w.addItems(["Red", "Green", "Blue"])
    w.setSelectedItems(["Red", "Blue"])
    assert sorted(w.selectedItems()) == ["Blue", "Red"]


def test_multi_select_clear(qtbot):
    w = StyledMultiSelectComboBox()
    qtbot.addWidget(w)
    w.addItems(["X", "Y"])
    w.setSelectedItems(["X"])
    w.clear()
    assert w.selectedItems() == []
    assert w._list.count() == 0


def test_multi_select_filter(qtbot):
    w = StyledMultiSelectComboBox()
    qtbot.addWidget(w)
    w.addItems(["Apple", "Banana", "Cherry", "Avocado"])
    # Open popup and filter for "av"
    w._search.setText("av")
    qtbot.wait(50)
    visible = [w._list.item(i).text() for i in range(w._list.count()) if not w._list.item(i).isHidden()]
    assert "Avocado" in visible
    assert "Apple" not in visible
    assert "Banana" not in visible
    assert "Cherry" not in visible


def test_multi_select_all(qtbot):
    w = StyledMultiSelectComboBox()
    qtbot.addWidget(w)
    w.addItems(["A", "B", "C", "D"])
    w._select_all()
    assert sorted(w.selectedItems()) == ["A", "B", "C", "D"]


def test_multi_deselect_all(qtbot):
    w = StyledMultiSelectComboBox()
    qtbot.addWidget(w)
    w.addItems(["X", "Y", "Z"])
    w.setSelectedItems(["X", "Y", "Z"])
    w._deselect_all()
    assert w.selectedItems() == []


def test_multi_select_all_respects_filter(qtbot):
    w = StyledMultiSelectComboBox()
    qtbot.addWidget(w)
    w.addItems(["Apple", "Banana", "Avocado", "Cherry"])
    # Filter to "av" then select all visible
    w._search.setText("av")
    qtbot.wait(50)
    w._select_all()
    # Only Avocado should be selected (filtered items not affected)
    assert w.selectedItems() == ["Avocado"]
