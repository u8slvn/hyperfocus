from __future__ import annotations

import importlib

import pytest

from hyperfocus.termui import style


@pytest.mark.parametrize(
    "platform, expected_colors",
    [
        (
            "windows",
            {
                "DEFAULT": "bright_white",
                "INFO": "blue",
                "SUCCESS": "bright_green",
                "STASHED": "magenta",
                "WARNING": "bright_yellow",
                "ERROR": "red",
                "UNKNOWN": "bright_black",
                "NEW_DAY": "blue",
                "BANNER": "cyan",
                "DELETED_TASK": "bright_black",
                "DONE_TASK": "strikethrough",
            },
        ),
        (
            "other",
            {
                "DEFAULT": "bright_white",
                "INFO": "steel_blue1",
                "SUCCESS": "chartreuse3",
                "STASHED": "purple4",
                "WARNING": "orange1",
                "ERROR": "red",
                "UNKNOWN": "bright_black",
                "NEW_DAY": "italic steel_blue1",
                "BANNER": "italic khaki1",
                "DELETED_TASK": "bright_black",
                "DONE_TASK": "strikethrough",
            },
        ),
    ],
)
def test_windows_style(mocker, platform, expected_colors):
    mocker.patch("hyperfocus.termui.style.sys.platform", platform)

    importlib.reload(style)

    for name, value in expected_colors.items():
        assert value == getattr(style, name)
