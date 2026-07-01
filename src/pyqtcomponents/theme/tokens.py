"""Color tokens — foundation palette and semantic mappings."""

from PySide6.QtGui import QColor


# ---------------------------------------------------------------------------
# Foundation: Primary (Blue)
# ---------------------------------------------------------------------------
PRIMARY_50 = QColor("#eff6ff")
PRIMARY_100 = QColor("#dbeafe")
PRIMARY_200 = QColor("#bfdbfe")
PRIMARY_300 = QColor("#93c5fd")
PRIMARY_400 = QColor("#60a5fa")
PRIMARY_500 = QColor("#3b82f6")
PRIMARY_600 = QColor("#3b82f6")
PRIMARY_700 = QColor("#2563eb")
PRIMARY_800 = QColor("#1d4ed8")
PRIMARY_900 = QColor("#1e40af")

# ---------------------------------------------------------------------------
# Foundation: Neutral (Slate)
# ---------------------------------------------------------------------------
NEUTRAL_50 = QColor("#f9fafb")
NEUTRAL_100 = QColor("#f3f4f6")
NEUTRAL_200 = QColor("#e5e7eb")
NEUTRAL_300 = QColor("#d1d5db")
NEUTRAL_400 = QColor("#9ca3af")
NEUTRAL_500 = QColor("#6b7280")
NEUTRAL_600 = QColor("#4b5563")
NEUTRAL_700 = QColor("#374151")
NEUTRAL_800 = QColor("#1f2937")
NEUTRAL_900 = QColor("#111827")

# ---------------------------------------------------------------------------
# Foundation: Semantic
# ---------------------------------------------------------------------------
SUCCESS = QColor("#22c55e")
WARNING = QColor("#f59e0b")
ERROR = QColor("#ef4444")

# ---------------------------------------------------------------------------
# Semantic tokens — light / dark values
# ---------------------------------------------------------------------------
_SEMANTIC_LIGHT = {
    "background-primary": QColor("#ffffff"),
    "background-secondary": QColor("#f9fafb"),
    "text-primary": QColor("#111827"),
    "text-secondary": QColor("#6b7280"),
    "border-default": QColor("#e5e7eb"),
    "highlight-focus": QColor("#3b82f6"),
}

_SEMANTIC_DARK = {
    "background-primary": QColor("#1f2937"),
    "background-secondary": QColor("#111827"),
    "text-primary": QColor("#f9fafb"),
    "text-secondary": QColor("#9ca3af"),
    "border-default": QColor("#374151"),
    "highlight-focus": QColor("#60a5fa"),
}


def semantic(token: str, dark: bool = False) -> QColor:
    """Look up a semantic color token by name."""
    table = _SEMANTIC_DARK if dark else _SEMANTIC_LIGHT
    try:
        return table[token]
    except KeyError:
        raise ValueError(f"Unknown semantic token: {token!r}") from None
