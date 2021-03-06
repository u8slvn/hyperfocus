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
    "kwargs, expected",
    [
        ({}, f"[{style.DEFAULT}]⬢[/] foo"),
        ({"show_prefix": True}, f"Task: #1 [{style.DEFAULT}]⬢[/] foo"),
    ],
)
def test_task(kwargs, expected):
    task = Task(id=1, title="foo", details="bar")

    pretty_task = formatter.task(task=task, **kwargs)

    assert pretty_task == expected


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
