import datetime

from hyperfocus.database.models import Task
from hyperfocus.termui import icons, printer


def test_banner(capsys):
    printer.banner("foobar")

    captured = capsys.readouterr()
    assert captured.out == "> foobar\n"


def test_new_day(capsys):
    printer.new_day(datetime.date(2022, 1, 1))

    captured = capsys.readouterr()
    assert (
        captured.out
        == f"> {icons.NEW_DAY} Sat, 01 January 2022: A new day starts, good luck!\n"
    )


def test_tasks(capsys):
    tasks = [
        Task(id=1, title="foo"),
        Task(id=1, title="bar", details="hello"),
    ]
    printer.tasks(tasks)

    expected = (
        "                       \n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        "  1   ⬢ foo      □     \n"
        "  1   ⬢ bar      ■     \n"
        "                       \n"
    )
    captured = capsys.readouterr()
    assert captured.out == expected


def test_progress_bar(capsys):
    tasks = [
        Task(title="foo"),
        Task(title="bar"),
    ]

    printer.progress_bar(tasks)

    expected = f" ⬢ 0% [{icons.PROGRESS_BAR_EMPTY * 30}]\n"
    captured = capsys.readouterr()
    assert captured.out == expected


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
