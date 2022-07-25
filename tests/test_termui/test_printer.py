import datetime

from hyperfocus.database.models import Task
from hyperfocus.termui import printer


def test_banner(capsys):
    printer.banner("foobar")

    captured = capsys.readouterr()
    assert captured.out == "> foobar\n"


def test_task_details(capsys):
    created_at = datetime.datetime(2022, 1, 1)
    task = Task(id=1, title="foo", created_at=created_at)

    printer.task_details(task)

    expected = (
        "Task: #1\n"
        "Status: ⬢ Todo\n"
        "Title: foo\n"
        "Details: ...\n"
        "History: \n"
        " • Sat, 01 January 2022 at 00:00:00 - add task\n"
    )
    captured = capsys.readouterr()
    assert captured.out == expected


def test_config(capsys):
    config = {
        "core.database": "/database.sqlite",
        "alias.st": "status",
    }

    printer.config(config)

    expected = "core.database = /database.sqlite\n" "alias.st = status\n"
    captured = capsys.readouterr()
    assert captured.out == expected
