"""Tests for WCAG contrast checker."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from PySide6.QtGui import QColor
from pyqtcomponents.theme.contrast import (
    relative_luminance, contrast_ratio,
    passes_aa_body, passes_aa_large, passes_aa_non_text,
    ContrastReport,
)


def test_relative_luminance_black():
    assert relative_luminance(QColor("#000000")) == 0.0


def test_relative_luminance_white():
    assert abs(relative_luminance(QColor("#ffffff")) - 1.0) < 0.01


def test_contrast_ratio_black_white():
    ratio = contrast_ratio(QColor("#000000"), QColor("#ffffff"))
    assert abs(ratio - 21.0) < 0.1


def test_contrast_ratio_same_color():
    ratio = contrast_ratio(QColor("#3b82f6"), QColor("#3b82f6"))
    assert ratio == 1.0


def test_passes_aa_body():
    assert passes_aa_body(4.5) is True
    assert passes_aa_body(4.4) is False
    assert passes_aa_body(7.0) is True


def test_passes_aa_large():
    assert passes_aa_large(3.0) is True
    assert passes_aa_large(2.9) is False
    assert passes_aa_large(4.5) is True


def test_passes_aa_non_text():
    assert passes_aa_non_text(3.0) is True
    assert passes_aa_non_text(2.5) is False


def test_contrast_report_pass():
    report = ContrastReport(QColor("#111827"), QColor("#ffffff"))
    assert report.passes_all is True
    assert report.ratio > 4.5


def test_contrast_report_fail():
    # Light gray on white should fail
    report = ContrastReport(QColor("#d1d5db"), QColor("#ffffff"))
    assert report.passes_all is False


def test_contrast_report_repr():
    report = ContrastReport(QColor("#000000"), QColor("#ffffff"))
    r = repr(report)
    assert "ContrastReport" in r
    assert "21.0" in r
