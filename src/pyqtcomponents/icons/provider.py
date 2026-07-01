"""Icon provider — loads SVG icons with size and color support.

Per spec D9:
- Sizes: xs (12px), sm (16px), md (24px), lg (32px)
- Format: SVG preferred, PNG fallback
- Color: inherits text color
- Naming: ic-{name}-{size}.svg
"""

from pathlib import Path
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPixmap, QPainter, QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication

from ..theme import tokens


# ---------------------------------------------------------------------------
# Size tokens
# ---------------------------------------------------------------------------
ICON_XS = 12
ICON_SM = 16
ICON_MD = 24
ICON_LG = 32

SIZE_MAP = {
    "xs": ICON_XS,
    "sm": ICON_SM,
    "md": ICON_MD,
    "lg": ICON_LG,
}

# Default icons directory (relative to package)
_DEFAULT_ICONS_DIR = Path(__file__).parent


class IconProvider:
    """Load and render SVG icons with size and color control.

    Usage::

        icons = IconProvider()
        icon = icons.get("file", size="md")          # QIcon
        pixmap = icons.get_pixmap("file", size="lg")  # QPixmap
    """

    def __init__(self, icons_dir: str | Path | None = None):
        self._dir = Path(icons_dir) if icons_dir else _DEFAULT_ICONS_DIR
        self._cache: dict[str, QPixmap] = {}

    def get(self, name: str, size: str | int = "md", color: QColor | None = None) -> QIcon:
        """Load an icon by name and return a QIcon.

        Args:
            name: Icon name (without size prefix or extension)
            size: Target size ("xs", "sm", "md", "lg") or pixel value
            color: Tint color (default: current text color)
        """
        px = self.get_pixmap(name, size, color)
        return QIcon(px)

    def get_pixmap(self, name: str, size: str | int = "md", color: QColor | None = None) -> QPixmap:
        """Load an icon and return a tinted QPixmap."""
        px_size = SIZE_MAP.get(size, size) if isinstance(size, str) else size
        cache_key = f"{name}_{px_size}_{color.name() if color else 'default'}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        # Resolve color
        if color is None:
            app = QApplication.instance()
            if app is not None:
                palette = app.palette()
                dark = palette.window().color().lightness() < 128
                color = tokens.NEUTRAL_50 if dark else tokens.NEUTRAL_900
            else:
                color = tokens.NEUTRAL_900

        # Try to find SVG
        svg_path = self._dir / f"ic-{name}-{px_size}.svg"
        if svg_path.exists():
            pixmap = self._render_svg(svg_path, px_size, color)
        else:
            # Fallback: try any size SVG
            matches = list(self._dir.glob(f"ic-{name}-*.svg"))
            if matches:
                pixmap = self._render_svg(matches[0], px_size, color)
            else:
                # Create empty placeholder
                pixmap = QPixmap(px_size, px_size)
                pixmap.fill(Qt.GlobalColor.transparent)

        self._cache[cache_key] = pixmap
        return pixmap

    def _render_svg(self, path: Path, size: int, color: QColor) -> QPixmap:
        """Render an SVG file to a tinted QPixmap."""
        renderer = QSvgRenderer(str(path))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        renderer.render(painter)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return pixmap

    def list_icons(self) -> list[str]:
        """List available icon names."""
        names = set()
        for f in self._dir.glob("ic-*.svg"):
            # ic-{name}-{size}.svg
            parts = f.stem.split("-")
            if len(parts) >= 3:
                names.add("-".join(parts[1:-1]))
        return sorted(names)
