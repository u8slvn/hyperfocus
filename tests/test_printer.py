import pytest

from hyperfocus.database.models import Task
from hyperfocus.termui import icons, printer


@pytest.mark.parametrize(
    "func, expected",
    [
        ("banner", "\x1b[3;38;5;228mfoobar\x1b[0m\n"),
        ("new_day", f"{icons.NEW_DAY} \x1b[38;5;81mfoobar\x1b[0m\n"),
    ],
)
def test_banner(capsys, func, expected):
    getattr(printer, func)("foobar")

    captured = capsys.readouterr()
    assert captured.out == expected


def test_tasks(capsys):
    tasks = [
        Task(id=1, title="foo"),
        Task(id=1, title="bar", details="hello"),
    ]
    printer.tasks(tasks)

    expected = (
        " ───────────────────── \n"
        "  #   tasks   details  \n"
        " ───────────────────── \n"
        "  1   ⬢ foo      □     \n"
        "  1   ⬢ bar      ■     \n"
        " ───────────────────── \n"
    )
    captured = capsys.readouterr()
    assert captured.out == expected
