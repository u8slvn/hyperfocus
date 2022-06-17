import datetime
from enum import Enum, auto
from typing import List

import click
from tabulate import tabulate

from hyperfocus.models import Status, Task


def date(date: datetime.date) -> str:
    return date.strftime("%a, %d %B %Y")


def task_status(task: Task):
    symbol = "⬢"
    color = {
        Status.TODO: "white",
        Status.BLOCKED: "bright_yellow",
        Status.DELETED: "red",
        Status.DONE: "green",
    }.get(Status(task.status), "black")

    return click.style(symbol, fg=color)


def task(task: Task, show_details: bool = False, show_prefix: bool = False) -> str:
    empty_details = "No details provided ..."

    title_style = {
        Status.DELETED: {"fg": "bright_black"},
        Status.DONE: {"strikethrough": True},
    }.get(Status(task.status), {})

    title = click.style(task.title, **title_style)  # type: ignore
    details = "⊕" if task.details else "◌"
    prefix = f"Task #{task.id} " if show_prefix else ""

    headline = f"{prefix}{task_status(task)} {title}"

    if show_details:
        return f"{headline}\n{task.details or empty_details}"

    return f"{headline} {details}"


def tasks(tasks: List[Task], newline: bool = False) -> str:
    headers = ["#", "tasks"]
    suffix = "\n" if newline else ""
    lines = [[t.id, task(t)] for t in tasks]

    return f"{tabulate(lines, headers)} {suffix}"


def prompt(text: str) -> str:
    symbol = click.style("?", fg="bright_green")
    return f"{symbol} {text}"


class NotificationStatus(Enum):
    SUCCESS = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


def notification(text: str, action: str, status: NotificationStatus) -> str:
    symbol, color = {
        NotificationStatus.SUCCESS: ("✔", "bright_green"),
        NotificationStatus.INFO: ("ℹ", "bright_cyan"),
        NotificationStatus.WARNING: ("▼", "bright_yellow"),
        NotificationStatus.ERROR: ("✘", "bright_red"),
    }.get(status, (">", "bright_white"))
    prefix = click.style(f"{symbol}({action})", fg=color)
    return f"{prefix} {text}"
