import datetime
from enum import Enum, auto
from typing import List

import typer
from tabulate import tabulate

from hyperfocus.models import Status, Task


def date(date: datetime.date) -> str:
    return date.strftime("%a, %d %B %Y")


def task_status(task: Task):
    symbol = "⬢"
    color = {
        Status.TODO: typer.colors.WHITE,
        Status.BLOCKED: typer.colors.BRIGHT_YELLOW,
        Status.DELETED: typer.colors.RED,
        Status.DONE: typer.colors.GREEN,
    }.get(Status(task.status), typer.colors.BLACK)

    return typer.style(symbol, fg=color)


def task(task: Task, show_details: bool = False, show_prefix: bool = False) -> str:
    empty_details = "No details provided ..."

    title_style = {
        Status.DELETED.value: {"fg": typer.colors.BRIGHT_BLACK},
        Status.DONE.value: {"strikethrough": True},
    }.get(task.status, {})

    title = typer.style(task.title, **title_style)
    details = "⊕" if task.details else "◌"
    prefix = f"Task #{task.id} " if show_prefix else ""

    headline = f"{prefix}{task_status(task)} {title}"

    if show_details:
        return f"{headline}\n{task.details or empty_details}"

    return f"{headline} {details}"


def tasks(tasks: List[Task], newline: bool = False) -> str:
    headers = ["#", "tasks"]
    suffix = "\n" if newline else ""
    tasks = [[t.id, task(t)] for t in tasks]

    return f"{tabulate(tasks, headers)} {suffix}"


def prompt(text: str) -> str:
    symbol = typer.style("?", fg=typer.colors.BRIGHT_GREEN)
    return f"{symbol} {text}"


class NotificationStatus(Enum):
    SUCCESS = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


def notification(text: str, action: str, status: NotificationStatus) -> str:
    symbol, color = {
        NotificationStatus.SUCCESS: ("✔", typer.colors.BRIGHT_GREEN),
        NotificationStatus.INFO: ("ℹ", typer.colors.BRIGHT_CYAN),
        NotificationStatus.WARNING: ("▼", typer.colors.BRIGHT_YELLOW),
        NotificationStatus.ERROR: ("✘", typer.colors.BRIGHT_RED),
    }.get(status, (">", typer.colors.BRIGHT_WHITE))
    prefix = typer.style(f"{symbol}({action})", fg=color)
    return f"{prefix} {text}"
