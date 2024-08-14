from __future__ import annotations

import click
import pytest

from hyperfocus.console.core.parameters import INT_LIST


@pytest.mark.parametrize(
    "value, expected",
    [
        ("1 2 3", [1, 2, 3]),
        ("1", [1]),
        ("", []),
        ([1, 2, 3], [1, 2, 3]),
    ],
)
def test_click_list_int_param_type_convert_success(value, expected):
    assert INT_LIST.convert(value, None, None) == expected


@pytest.mark.parametrize(
    "value",
    [
        "a",
        1,
        {"a": 1},
    ],
)
def test_click_list_int_param_type_convert_fails(value):
    with pytest.raises(click.BadParameter):
        INT_LIST.convert(value, None, None)
