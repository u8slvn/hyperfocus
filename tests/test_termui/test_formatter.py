import datetime

import pytest

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.termui import formatter, icons, style


def test_formatter_date():
    date = datetime.datetime(2012, 1, 14)

    pretty_date = formatter.date(date=date)

    expected = "Sat, 14 January 2012"
    assert pretty_date == expected


@pytest.mark.parametrize(
    "status, expected",
    [
        (TaskStatus.TODO, f"[{style.DEFAULT}]{icons.TASK_STATUS}[/]"),
        (TaskStatus.DELETED, f"[{style.ERROR}]{icons.TASK_STATUS}[/]"),
        (TaskStatus.DONE, f"[{style.SUCCESS}]{icons.TASK_STATUS}[/]"),
    ],
)
def test_formatter_task_status(status, expected):
    pretty_status = formatter.task_status(status)

    assert pretty_status == expected


@pytest.mark.parametrize(
    "formatter_args, expected",
    [
        ({}, f"[{style.DEFAULT}]⬢[/] Test"),
        ({"show_prefix": True}, f"Task: #1 [{style.DEFAULT}]⬢[/] Test"),
        (
            {"show_details": True},
            f"[{style.DEFAULT}]⬢[/] Test\nNo details provided ...",
        ),
        (
            {"show_details": True, "show_prefix": True},
            f"Task: #1 [{style.DEFAULT}]⬢[/] Test\nNo details provided ...",
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
        ({}, f"[{style.DEFAULT}]⬢[/] Test"),
        ({"show_prefix": True}, f"Task: #1 [{style.DEFAULT}]⬢[/] Test"),
        ({"show_details": True}, f"[{style.DEFAULT}]⬢[/] Test\nHello"),
        (
            {"show_details": True, "show_prefix": True},
            f"Task: #1 [{style.DEFAULT}]⬢[/] Test\nHello",
        ),
    ],
)
def test_formatter_task_with_details(pretty_args, expected):
    task = Task(id=1, title="Test", details="Hello")

    pretty_task = formatter.task(task=task, **pretty_args)

    assert pretty_task == expected


def test_formatter_prompt():
    text = "Test prompt"

    formatter_prompt = formatter.prompt(text=text)

    expected = f"[{style.SUCCESS}]{icons.PROMPT}[/] Test prompt"
    assert formatter_prompt == expected


@pytest.mark.parametrize(
    "status, expected",
    [
        (
            formatter.NotificationLevel.SUCCESS,
            f"[{style.SUCCESS}]{icons.NOTIFICATION_SUCCESS}(test)[/] Test",
        ),
        (
            formatter.NotificationLevel.INFO,
            f"[{style.INFO}]{icons.NOTIFICATION_INFO}(test)[/] Test",
        ),
        (
            formatter.NotificationLevel.WARNING,
            f"[{style.WARNING}]{icons.NOTIFICATION_WARNING}(test)[/] Test",
        ),
        (
            formatter.NotificationLevel.ERROR,
            f"[{style.ERROR}]{icons.NOTIFICATION_ERROR}(test)[/] Test",
        ),
    ],
)
def test_formatter_notification(status, expected):
    text = "Test"
    action = "test"

    formatted_notification = formatter.notification(
        text=text, event=action, status=status
    )

    assert formatted_notification == expected


def test_task_details():
    created_at = datetime.datetime(2022, 1, 1)
    task1 = Task(title="foo", created_at=created_at)
    task2 = Task(title="bar", parent_task=task1, created_at=created_at)
    task3 = Task(id=3, title="foobar", parent_task=task2, created_at=created_at)

    task_details = formatter.task_details(task3)

    expected = (
        f"[{style.INFO}]Task[/]: #3\n"
        f"[{style.INFO}]Status[/]: "
        f"[{style.DEFAULT}]{icons.TASK_STATUS}[/] Todo\n"
        f"[{style.INFO}]Title[/]: foobar\n"
        f"[{style.INFO}]Details[/]: ...\n"
        f"[{style.INFO}]History[/]: \n"
        f" [{style.INFO}]•[/] Sat, 01 January 2022 at 00:00:00 - add task\n"
        f" [{style.INFO}]•[/] Sat, 01 January 2022 at 00:00:00 - recover task\n"
        f" [{style.INFO}]•[/] Sat, 01 January 2022 at 00:00:00 -"
        f" initial task creation"
    )
    assert task_details == expected


def test_config():
    config = {
        "core.database": "/database.sqlite",
        "alias.st": "status",
    }

    result = formatter.config(config)

    expected = (
        f"[{style.INFO}]core.database[/] = /database.sqlite\n"
        f"[{style.INFO}]alias.st[/] = status"
    )
    assert result == expected
