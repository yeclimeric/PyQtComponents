"""WCAG 2.1 AA contrast ratio checker.

Per spec D12:
- Body text: >= 4.5:1
- Large text (18px+): >= 3:1
- Non-text elements: >= 3:1
- Focus indicators: >= 3:1
"""

from PySide6.QtGui import QColor


def relative_luminance(color: QColor) -> float:
    """Calculate relative luminance of a color per WCAG 2.1.

    See: https://www.w3.org/TR/WCAG21/#dfn-relative-luminance
    """
    r, g, b = color.redF(), color.greenF(), color.blueF()

    def linearize(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(color1: QColor, color2: QColor) -> float:
    """Calculate contrast ratio between two colors.

    Returns a value between 1:1 (identical) and 21:1 (black vs white).
    """
    l1 = relative_luminance(color1)
    l2 = relative_luminance(color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def passes_aa_body(ratio: float) -> bool:
    """Check if contrast ratio passes WCAG AA for body text (>= 4.5:1)."""
    return ratio >= 4.5


def passes_aa_large(ratio: float) -> bool:
    """Check if contrast ratio passes WCAG AA for large text (>= 3:1)."""
    return ratio >= 3.0


def passes_aa_non_text(ratio: float) -> bool:
    """Check if contrast ratio passes WCAG AA for non-text elements (>= 3:1)."""
    return ratio >= 3.0


class ContrastReport:
    """Report contrast compliance for a pair of colors.

    Usage::

        report = ContrastReport(QColor("#111827"), QColor("#ffffff"))
        print(report)  # shows ratio and pass/fail for each category
    """

    def __init__(self, foreground: QColor, background: QColor):
        self.foreground = foreground
        self.background = background
        self.ratio = contrast_ratio(foreground, background)
        self.body_text = passes_aa_body(self.ratio)
        self.large_text = passes_aa_large(self.ratio)
        self.non_text = passes_aa_non_text(self.ratio)

    @property
    def passes_all(self) -> bool:
        return self.body_text and self.large_text and self.non_text

    def __repr__(self) -> str:
        status = "PASS" if self.passes_all else "FAIL"
        return (
            f"ContrastReport({self.foreground.name()} on {self.background.name()}: "
            f"{self.ratio:.2f}:1 [{status}] "
            f"body={self.body_text} large={self.large_text} non_text={self.non_text})"
        )
