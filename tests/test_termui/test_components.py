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
    TaskDetails,
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
        f"  1   {icons.TASK_STATUS} foo      {icons.NO_DETAILS}     \n"
        f"  1   {icons.TASK_STATUS} bar      {icons.DETAILS}     \n"
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


def test_task_details(capsys):
    created_at = datetime.datetime(2022, 1, 1)
    task1 = Task(id=1, title="foo", created_at=created_at)
    task2 = Task(id=1, title="foo", created_at=created_at, parent_task=task1)
    task3 = Task(id=1, title="foo", created_at=created_at, parent_task=task2)

    printer.echo(TaskDetails(task3))

    expected = (
        "Task: #1\n"
        f"Status: {icons.TASK_STATUS} Todo\n"
        "Title: foo\n"
        "Details: ...\n"
        "History: \n"
        " • Sat, 01 January 2022 at 00:00:00 - add task\n"
        " • Sat, 01 January 2022 at 00:00:00 - continue task\n"
        " • Sat, 01 January 2022 at 00:00:00 - create task\n"
    )
    captured = capsys.readouterr()
    assert captured.out == expected
