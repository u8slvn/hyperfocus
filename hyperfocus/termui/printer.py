from __future__ import annotations

import datetime
from typing import cast

import click

from hyperfocus.database.models import Task
from hyperfocus.termui import formatter, icons, style
from hyperfocus.termui.components import UIComponent
from hyperfocus.termui.markup import markup


def echo(text: str | UIComponent, nl: bool = True) -> None:
    if isinstance(text, UIComponent):
        text = cast(str, text.resolve())
    click.echo(markup.resolve(text), nl=nl)


def task(task: Task, show_details: bool = False, show_prefix: bool = False) -> None:
    formatted_task = formatter.task(
        task=task, show_details=show_details, show_prefix=show_prefix
    )
    echo(text=formatted_task)


def task_details(task: Task) -> None:
    echo(formatter.task_details(task))


def notification(text: str, event: str, status: formatter.NotificationLevel) -> None:
    formatted_notification = formatter.notification(
        text=text, event=event, status=status
    )
    echo(text=formatted_notification)


def info(text: str, event: str) -> None:
    notification(text=text, event=event, status=formatter.NotificationLevel.INFO)


def success(text: str, event: str) -> None:
    notification(text=text, event=event, status=formatter.NotificationLevel.SUCCESS)


def warning(text: str, event: str) -> None:
    notification(text=text, event=event, status=formatter.NotificationLevel.WARNING)


def error(text: str, event: str) -> None:
    notification(text=text, event=event, status=formatter.NotificationLevel.ERROR)


def banner(text: str) -> None:
    echo(f"[{style.BANNER}]> {text}[/]")


def new_day(date: datetime.date) -> None:
    echo(
        f"[{style.NEW_DAY}]> {icons.NEW_DAY} {formatter.date(date)}: "
        f"A new day starts, good luck![/]"
    )


def progress_bar(tasks: list[Task]) -> None:
    echo(formatter.progress_bar(tasks), nl=False)


def config(config: dict[str, str]) -> None:
    echo(formatter.config(config))
