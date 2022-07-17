from datetime import datetime

import pytest
from freezegun import freeze_time

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.termui import formatter, icons


@freeze_time("2012-01-14")
def test_formatter_date():
    date = datetime.now().date()

    pretty_date = formatter.date(date=date)

    expected = "Sat, 14 January 2012"
    assert pretty_date == expected


@pytest.mark.parametrize(
    "status, expected",
    [
        (TaskStatus.TODO, f"[bright_white]{icons.TASK_STATUS}[/]"),
        (TaskStatus.BLOCKED, f"[orange1]{icons.TASK_STATUS}[/]"),
        (TaskStatus.DELETED, f"[deep_pink2]{icons.TASK_STATUS}[/]"),
        (TaskStatus.DONE, f"[chartreuse3]{icons.TASK_STATUS}[/]"),
    ],
)
def test_formatter_task_status(status, expected):
    pretty_status = formatter.task_status(status)

    assert pretty_status == expected


@pytest.mark.parametrize(
    "formatter_args, expected",
    [
        ({}, "[bright_white]⬢[/] Test"),
        ({"show_prefix": True}, "Task: #1 [bright_white]⬢[/] Test"),
        (
            {"show_details": True},
            "[bright_white]⬢[/] Test\nNo details provided ...",
        ),
        (
            {"show_details": True, "show_prefix": True},
            "Task: #1 [bright_white]⬢[/] Test\nNo details provided ...",
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
        ({}, "[bright_white]⬢[/] Test"),
        ({"show_prefix": True}, "Task: #1 [bright_white]⬢[/] Test"),
        ({"show_details": True}, "[bright_white]⬢[/] Test\nHello"),
        (
            {"show_details": True, "show_prefix": True},
            "Task: #1 [bright_white]⬢[/] Test\nHello",
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

    expected = f"[chartreuse3]{icons.PROMPT}[/] Test prompt"
    assert formatter_prompt == expected


@pytest.mark.parametrize(
    "status, expected",
    [
        (
            formatter.NotificationLevel.SUCCESS,
            f"[chartreuse3]{icons.NOTIFICATION_SUCCESS}(test)[/] Test",
        ),
        (
            formatter.NotificationLevel.INFO,
            f"[steel_blue1]{icons.NOTIFICATION_INFO}(test)[/] Test",
        ),
        (
            formatter.NotificationLevel.WARNING,
            f"[orange1]{icons.NOTIFICATION_WARNING}(test)[/] Test",
        ),
        (
            formatter.NotificationLevel.ERROR,
            f"[deep_pink2]{icons.NOTIFICATION_ERROR}(test)[/] Test",
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


@pytest.mark.parametrize(
    "tasks, expected",
    [
        (
            [
                Task(title="foo"),
                Task(title="foo", status=TaskStatus.DONE),
            ],
            (
                f"[chartreuse3]50% [{icons.PROGRESS_BAR * 15}[/]"
                f"[bright_white]{icons.PROGRESS_BAR * 15}] 50%[/]"
            ),
        ),
        (
            [
                Task(title="foo"),
                Task(title="foo"),
                Task(title="foo", status=TaskStatus.DONE),
            ],
            (
                f"[chartreuse3]33% [{icons.PROGRESS_BAR * 10}[/]"
                f"[bright_white]{icons.PROGRESS_BAR * 20}] 66%[/]"
            ),
        ),
    ],
)
def test_progress_bar(tasks, expected):
    progress_bar = formatter.progress_bar(tasks)

    assert progress_bar == expected
