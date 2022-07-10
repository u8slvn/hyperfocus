from __future__ import annotations

from typing import Any, List

import click

from hyperfocus import formatter
from hyperfocus.database.models import Task


def echo(text: str):
    click.secho(text)


def task(task: Task, show_details: bool = False, show_prefix: bool = False):
    formatted_task = formatter.task(
        task=task, show_details=show_details, show_prefix=show_prefix
    )
    echo(text=formatted_task)


def tasks(tasks: List[Task], newline: bool = False):
    formatted_tasks = formatter.tasks(tasks=tasks, newline=newline)
    echo(text=formatted_tasks)


def notification(text: str, event: str, status: formatter.NotificationLevel):
    formatted_notification = formatter.notification(
        text=text, event=event, status=status
    )
    echo(text=formatted_notification)


def info(text: str, event: str):
    notification(text=text, event=event, status=formatter.NotificationLevel.INFO)


def success(text: str, event: str):
    notification(text=text, event=event, status=formatter.NotificationLevel.SUCCESS)


def warning(text: str, event: str):
    notification(text=text, event=event, status=formatter.NotificationLevel.WARNING)


def error(text: str, event: str):
    notification(text=text, event=event, status=formatter.NotificationLevel.ERROR)


def ask(text: str, **kwargs) -> Any:
    formatted_prompt = formatter.prompt(text=text)
    return click.prompt(text=formatted_prompt, **kwargs)


def confirm(text: str, **kwargs) -> Any:
    formatted_prompt = formatter.prompt(text=text)
    return click.confirm(text=formatted_prompt, **kwargs)
