from __future__ import annotations

import datetime
from typing import Any, List

import rich
from rich.box import Box
from rich.console import Console
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from rich.theme import Theme

from hyperfocus.database.models import Task
from hyperfocus.termui import formatter, icons, style


theme = Theme(
    {
        "prompt.invalid": style.ERROR,
        "prompt.invalid.choice": style.ERROR,
    }
)

console = Console(highlight=False, force_terminal=True, theme=theme)

CUSTOM_BOX: Box = Box(
    "\n".join(
        [
            "    ",
            "    ",
            " -- ",
            "    ",
            "    ",
            "    ",
            "    ",
            "    ",
        ]
    )
)


def echo(text: str) -> None:
    console.print(text)


def task(task: Task, show_details: bool = False, show_prefix: bool = False) -> None:
    formatted_task = formatter.task(
        task=task, show_details=show_details, show_prefix=show_prefix
    )
    echo(text=formatted_task)


def task_details(task: Task) -> None:
    echo(formatter.task_details(task))


def tasks(tasks: List[Task]) -> None:
    table = Table(
        box=CUSTOM_BOX,
    )
    table.add_column("#", justify="right")
    table.add_column("tasks")
    table.add_column("details", justify="center")
    for task in tasks:
        details = icons.DETAILS if task.details else icons.NO_DETAILS
        table.add_row(str(task.id), formatter.task(task), details)
    rich.print(table, end="")


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


def ask(text: str, **kwargs) -> Any:
    text = formatter.prompt(text)
    return Prompt(console=console).ask(text, **kwargs)


def ask_int(text: str, **kwargs) -> Any:
    text = formatter.prompt(text)
    return IntPrompt(console=console).ask(text, **kwargs)


def confirm(text: str, **kwargs) -> Any:
    text = formatter.prompt(text)
    return Confirm(console=console).ask(text, **kwargs)


def banner(text: str) -> None:
    echo(f"[{style.BANNER}]> {text}[/]")


def new_day(date: datetime.date) -> None:
    echo(
        f"[{style.NEW_DAY}]> {icons.NEW_DAY} {formatter.date(date)}: "
        f"A new day starts, good luck![/]"
    )


def progress_bar(tasks: list[Task]) -> None:
    echo(formatter.progress_bar(tasks))
