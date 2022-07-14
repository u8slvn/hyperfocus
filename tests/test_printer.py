import pytest

from hyperfocus.termui import icons, printer


@pytest.mark.parametrize(
    "func, expected",
    [
        ("banner", "foobar\n"),
        ("new_day", f"{icons.NEW_DAY} foobar\n"),
    ],
)
def test_banner(capsys, func, expected):
    getattr(printer, func)("foobar")

    captured = capsys.readouterr()
    assert captured.out == expected
