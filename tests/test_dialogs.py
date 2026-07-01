"""Smoke tests for styled dialogs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyqtcomponents.widgets.dialogs import StyledMessageBox, StyledInputDialog


def test_message_box_info_exists(qtbot):
    assert hasattr(StyledMessageBox, "info")
    assert callable(StyledMessageBox.info)


def test_message_box_warning_exists(qtbot):
    assert hasattr(StyledMessageBox, "warning")
    assert callable(StyledMessageBox.warning)


def test_message_box_error_exists(qtbot):
    assert hasattr(StyledMessageBox, "error")
    assert callable(StyledMessageBox.error)


def test_message_box_question_exists(qtbot):
    assert hasattr(StyledMessageBox, "question")
    assert callable(StyledMessageBox.question)


def test_input_dialog_text_exists(qtbot):
    assert hasattr(StyledInputDialog, "text")
    assert callable(StyledInputDialog.text)


def test_input_dialog_integer_exists(qtbot):
    assert hasattr(StyledInputDialog, "integer")
    assert callable(StyledInputDialog.integer)


def test_input_dialog_double_exists(qtbot):
    assert hasattr(StyledInputDialog, "double")
    assert callable(StyledInputDialog.double)


def test_input_dialog_choice_exists(qtbot):
    assert hasattr(StyledInputDialog, "choice")
    assert callable(StyledInputDialog.choice)
