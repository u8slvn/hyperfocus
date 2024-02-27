from __future__ import annotations

import sys


if sys.platform.startswith("win"):
    DEFAULT = "bright_white"
    INFO = "blue"
    SUCCESS = "bright_green"
    STASHED = "magenta"
    WARNING = "bright_yellow"
    ERROR = "red"
    UNKNOWN = "bright_black"

    NEW_DAY = f"{INFO}"
    BANNER = "cyan"

    DELETED_TASK = f"{UNKNOWN}"
    DONE_TASK = "strikethrough"
else:
    DEFAULT = "bright_white"
    INFO = "steel_blue1"
    SUCCESS = "chartreuse3"
    STASHED = "purple4"
    WARNING = "orange1"
    ERROR = "red"
    UNKNOWN = "bright_black"

    NEW_DAY = f"italic {INFO}"
    BANNER = "italic khaki1"

    DELETED_TASK = f"{UNKNOWN}"
    DONE_TASK = "strikethrough"
