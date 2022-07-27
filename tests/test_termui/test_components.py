import datetime

import pytest

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.termui import icons, printer
from hyperfocus.termui.components import (
    ErrorNotification,
    InfoNotification,
    NewDay,
    Notification,
    ProgressBar,
    SuccessNotification,
    TasksTable,
    WarningNotification,
)


def test_tasks_table(capsys):
    tasks = [
        Task(id=1, title="foo"),
        Task(id=1, title="bar", details="hello"),
    ]
    printer.echo(TasksTable(tasks))

    expected = (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        "  1   ⬢ foo      □     \n"
        "  1   ⬢ bar      ■     \n"
        "\n"
    )
    captured = capsys.readouterr()
    assert captured.out == expected


def test_progress_bar(capsys):
    tasks = [
        Task(title="foo"),
        Task(title="bar", status=TaskStatus.DONE),
    ]

    printer.echo(ProgressBar(tasks))

    expected = (
        f" {icons.TASK_STATUS} 50% [{icons.PROGRESSBAR * 15}"
        f"{icons.PROGRESSBAR_EMPTY * 15}]\n\n"
    )
    captured = capsys.readouterr()
    assert captured.out == expected


def test_progress_bar_with_no_tasks(capsys):
    tasks = []

    printer.echo(ProgressBar(tasks), nl=False)

    captured = capsys.readouterr()
    assert captured.out == ""


def test_new_day(capsys):
    date = datetime.date(2022, 1, 1)

    printer.echo(NewDay(date))

    expected = f"> {icons.NEW_DAY} Sat, 01 January 2022: A new day starts, good luck!\n"
    captured = capsys.readouterr()
    assert captured.out == expected


@pytest.mark.parametrize(
    "notification, expected",
    [
        (Notification, f"{icons.NOTIFICATION}(bar) foo\n"),
        (SuccessNotification, f"{icons.NOTIFICATION_SUCCESS}(bar) foo\n"),
        (InfoNotification, f"{icons.NOTIFICATION_INFO}(bar) foo\n"),
        (WarningNotification, f"{icons.NOTIFICATION_WARNING}(bar) foo\n"),
        (ErrorNotification, f"{icons.NOTIFICATION_ERROR}(bar) foo\n"),
    ],
)
def test_notification(capsys, notification, expected):
    printer.echo(notification(text="foo", event="bar"))

    captured = capsys.readouterr()
    assert captured.out == expected
