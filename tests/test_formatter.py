from datetime import datetime

import pytest
from freezegun import freeze_time

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.termui import formatter


@freeze_time("2012-01-14")
def test_formatter_date():
    date = datetime.now().date()

    pretty_date = formatter.date(date=date)

    expected = "Sat, 14 January 2012"
    assert pretty_date == expected


@pytest.mark.parametrize(
    "status, expected",
    [
        (TaskStatus.TODO, "\x1b[37m⬢\x1b[0m"),
        (TaskStatus.BLOCKED, "\x1b[93m⬢\x1b[0m"),
        (TaskStatus.DELETED, "\x1b[31m⬢\x1b[0m"),
        (TaskStatus.DONE, "\x1b[32m⬢\x1b[0m"),
    ],
)
def test_formatter_task_status(status, expected):
    pretty_status = formatter.task_status(status)

    assert pretty_status == expected


@pytest.mark.parametrize(
    "formatter_args, expected",
    [
        ({}, "\x1b[37m⬢\x1b[0m Test\x1b[0m ◌"),
        ({"show_prefix": True}, "Task: #1 \x1b[37m⬢\x1b[0m Test\x1b[0m ◌"),
        (
            {"show_details": True},
            "\x1b[37m⬢\x1b[0m Test\x1b[0m\nNo details provided ...",
        ),
        (
            {"show_details": True, "show_prefix": True},
            "Task: #1 \x1b[37m⬢\x1b[0m Test\x1b[0m\nNo details provided ...",
        ),
    ],
)
def test_formatter_task_with_no_details(formatter_args, expected):
    task = Task(id=1, title="Test")

    formatted_task = formatter.task(task=task, **formatter_args)

    assert formatted_task == expected


@pytest.mark.parametrize(
    "pretty_args, expected",
    [
        ({}, "\x1b[37m⬢\x1b[0m Test\x1b[0m ⊕"),
        ({"show_prefix": True}, "Task: #1 \x1b[37m⬢\x1b[0m Test\x1b[0m ⊕"),
        ({"show_details": True}, "\x1b[37m⬢\x1b[0m Test\x1b[0m\nHello"),
        (
            {"show_details": True, "show_prefix": True},
            "Task: #1 \x1b[37m⬢\x1b[0m Test\x1b[0m\nHello",
        ),
    ],
)
def test_formatter_task_with_details(pretty_args, expected):
    task = Task(id=1, title="Test", details="Hello")

    pretty_task = formatter.task(task=task, **pretty_args)

    assert pretty_task == expected


def test_formatter_tasks():
    tasks = [
        Task(id=1, title="Test", details="new"),
        Task(id=2, title="Test", status=TaskStatus.DELETED),
        Task(id=3, title="Test", status=TaskStatus.DONE),
    ]

    formatted_tasks = formatter.tasks(tasks=tasks)

    expected = (
        "  #  tasks\n"
        "---  --------\n"
        "  1  \x1b[37m⬢\x1b[0m Test\x1b[0m ⊕\n"
        "  2  \x1b[31m⬢\x1b[0m \x1b[90mTest\x1b[0m ◌\n"
        "  3  \x1b[32m⬢\x1b[0m \x1b[9mTest\x1b[0m ◌ "
    )
    assert formatted_tasks == expected


def test_formatter_tasks_with_newline():
    tasks = [
        Task(id=1, title="Test"),
    ]

    formatted_tasks = formatter.tasks(tasks=tasks, newline=True)

    expected = "  #  tasks\n" "---  --------\n" "  1  \x1b[37m⬢\x1b[0m Test\x1b[0m ◌ \n"
    assert formatted_tasks == expected


def test_formatter_prompt():
    text = "Test prompt"

    formatter_prompt = formatter.prompt(text=text)

    expected = "\x1b[92m?\x1b[0m Test prompt"
    assert formatter_prompt == expected


@pytest.mark.parametrize(
    "status, expected",
    [
        (formatter.NotificationLevel.SUCCESS, "\x1b[92m✔(test)\x1b[0m Test"),
        (formatter.NotificationLevel.INFO, "\x1b[96mℹ(test)\x1b[0m Test"),
        (formatter.NotificationLevel.WARNING, "\x1b[93m▼(test)\x1b[0m Test"),
        (formatter.NotificationLevel.ERROR, "\x1b[91m✘(test)\x1b[0m Test"),
    ],
)
def test_formatter_notification(status, expected):
    text = "Test"
    action = "test"

    formatted_notification = formatter.notification(
        text=text, event=action, status=status
    )

    assert formatted_notification == expected
