from datetime import datetime

import pytest
from freezegun import freeze_time

from hyperfocus import printer
from hyperfocus.models import Status, Task


@freeze_time("2012-01-14")
def test_pretty_date(tmp_test_dir):
    date = datetime.now().date()

    pretty_date = printer.date(date=date)

    expected = "Sat, 14 January 2012"
    assert expected == pretty_date


@pytest.mark.parametrize(
    "status, expected",
    [
        (Status.TODO, "\x1b[37m⬢\x1b[0m"),
        (Status.BLOCKED, "\x1b[93m⬢\x1b[0m"),
        (Status.DELETED, "\x1b[31m⬢\x1b[0m"),
        (Status.DONE, "\x1b[32m⬢\x1b[0m"),
    ],
)
def test_pretty_task_status(status, expected):
    task = Task(title="", status=status)

    pretty_status = printer.task_status(task)

    assert expected == pretty_status


@pytest.mark.parametrize(
    "pretty_args, expected",
    [
        ({}, "\x1b[37m⬢\x1b[0m Test\x1b[0m ◌"),
        ({"show_prefix": True}, "Task #1 \x1b[37m⬢\x1b[0m Test\x1b[0m ◌"),
        (
            {"show_details": True},
            "\x1b[37m⬢\x1b[0m Test\x1b[0m\nNo details provided ...",
        ),
        (
            {"show_details": True, "show_prefix": True},
            "Task #1 \x1b[37m⬢\x1b[0m Test\x1b[0m\nNo details provided ...",
        ),
    ],
)
def test_pretty_task_with_no_details(pretty_args, expected):
    task = Task(id=1, title="Test")

    pretty_task = printer.task(task=task, **pretty_args)

    assert expected == pretty_task


@pytest.mark.parametrize(
    "pretty_args, expected",
    [
        ({}, "\x1b[37m⬢\x1b[0m Test\x1b[0m ⊕"),
        ({"show_prefix": True}, "Task #1 \x1b[37m⬢\x1b[0m Test\x1b[0m ⊕"),
        ({"show_details": True}, "\x1b[37m⬢\x1b[0m Test\x1b[0m\nHello"),
        (
            {"show_details": True, "show_prefix": True},
            "Task #1 \x1b[37m⬢\x1b[0m Test\x1b[0m\nHello",
        ),
    ],
)
def test_pretty_task_with_details(pretty_args, expected):
    task = Task(id=1, title="Test", details="Hello")

    pretty_task = printer.task(task=task, **pretty_args)

    assert expected == pretty_task


def test_pretty_tasks():
    tasks = [
        Task(id=1, title="Test", details="new"),
        Task(id=2, title="Test", status=Status.DELETED),
        Task(id=3, title="Test", status=Status.DONE),
    ]

    pretty_tasks = printer.tasks(tasks=tasks)

    expected = (
        "  #  tasks\n"
        "---  --------\n"
        "  1  \x1b[37m⬢\x1b[0m Test\x1b[0m ⊕\n"
        "  2  \x1b[31m⬢\x1b[0m Test\x1b[0m ◌\n"
        "  3  \x1b[32m⬢\x1b[0m Test\x1b[0m ◌ "
    )
    assert expected == pretty_tasks


def test_pretty_tasks_with_newline():
    tasks = [
        Task(id=1, title="Test"),
    ]

    pretty_tasks = printer.tasks(tasks=tasks, newline=True)

    expected = "  #  tasks\n" "---  --------\n" "  1  \x1b[37m⬢\x1b[0m Test\x1b[0m ◌ \n"
    assert expected == pretty_tasks


def test_pretty_prompt():
    text = "Test prompt"

    pretty_prompt = printer.prompt(text=text)

    expected = "\x1b[92m?\x1b[0m Test prompt"
    assert expected == pretty_prompt


@pytest.mark.parametrize(
    "status, expected",
    [
        (printer.NotificationStatus.SUCCESS, "\x1b[92m✔(test)\x1b[0m Test"),
        (printer.NotificationStatus.INFO, "\x1b[96mℹ(test)\x1b[0m Test"),
        (printer.NotificationStatus.WARNING, "\x1b[93m▼(test)\x1b[0m Test"),
        (printer.NotificationStatus.ERROR, "\x1b[91m✘(test)\x1b[0m Test"),
    ],
)
def test_pretty_notification(status, expected):
    text = "Test"
    action = "test"

    pretty_notification = printer.notification(text=text, action=action, status=status)

    assert expected == pretty_notification
