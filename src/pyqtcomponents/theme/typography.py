"""Typography tokens — system font stacks and size scale."""

import sys

# ---------------------------------------------------------------------------
# Font families (by platform)
# ---------------------------------------------------------------------------
if sys.platform == "darwin":
    SANS_SERIF = "'SF Pro Text', 'Helvetica Neue', Arial"
    MONOSPACE = "'SF Mono', 'Cascadia Code', 'JetBrains Mono'"
elif sys.platform == "win32":
    SANS_SERIF = "'Segoe UI', 'Microsoft YaHei'"
    MONOSPACE = "'Cascadia Code', 'Consolas'"
else:
    SANS_SERIF = "'Noto Sans', 'Ubuntu', sans-serif"
    MONOSPACE = "'Cascadia Code', 'JetBrains Mono', monospace"

# ---------------------------------------------------------------------------
# Font sizes (px)
# ---------------------------------------------------------------------------
XS = 11
SM = 12
BASE = 13
LG = 14
XL = 16
XXL = 20
