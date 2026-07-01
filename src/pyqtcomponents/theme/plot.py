"""Plot theme — colors, grid, and line palette for data visualization.

Per spec D8: high contrast + configurable grid strategy.
Data line colors are colorblind-friendly (Okabe-Ito palette).
"""

from PySide6.QtGui import QColor

from . import tokens


# ---------------------------------------------------------------------------
# Data line colors (colorblind-friendly, Okabe-Ito palette)
# ---------------------------------------------------------------------------
DATA_LINE_COLORS = [
    QColor("#E69F00"),  # Orange
    QColor("#56B4E9"),  # Sky blue
    QColor("#009E73"),  # Bluish green
    QColor("#F0E442"),  # Yellow
    QColor("#0072B2"),  # Blue
    QColor("#D55E00"),  # Vermilion
    QColor("#CC79A7"),  # Reddish purple
]

DATA_LINE_COLORS_HEX = [c.name() for c in DATA_LINE_COLORS]


class PlotTheme:
    """Configurable plot area theme.

    Usage::

        theme = PlotTheme()
        cfg = theme.light()   # or theme.dark()
        ax.set_facecolor(cfg.background)
        ax.tick_params(colors=cfg.axis_text)
        ax.grid(True, color=cfg.grid_color, alpha=cfg.grid_opacity)
    """

    def __init__(self):
        pass

    def light(self) -> "PlotConfig":
        """Return plot config for light mode."""
        return PlotConfig(
            background=QColor("#ffffff"),
            grid_color=tokens.NEUTRAL_300,
            grid_opacity=0.3,
            axis_text=tokens.NEUTRAL_700,
            data_colors=list(DATA_LINE_COLORS),
        )

    def dark(self) -> "PlotConfig":
        """Return plot config for dark mode."""
        return PlotConfig(
            background=QColor("#2d2d2d"),
            grid_color=tokens.NEUTRAL_600,
            grid_opacity=0.3,
            axis_text=tokens.NEUTRAL_300,
            data_colors=list(DATA_LINE_COLORS),
        )


class PlotConfig:
    """Immutable plot configuration snapshot."""

    __slots__ = ("background", "grid_color", "grid_opacity", "axis_text", "data_colors")

    def __init__(
        self,
        background: QColor,
        grid_color: QColor,
        grid_opacity: float,
        axis_text: QColor,
        data_colors: list[QColor],
    ):
        self.background = background
        self.grid_color = grid_color
        self.grid_opacity = grid_opacity
        self.axis_text = axis_text
        self.data_colors = data_colors

    def line_color(self, index: int) -> QColor:
        """Get data line color by index, cycling if needed."""
        return self.data_colors[index % len(self.data_colors)]
