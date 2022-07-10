from __future__ import annotations

import datetime
from enum import Enum, IntEnum, auto
from typing import List

import click
from tabulate import tabulate

from hyperfocus.database.models import Task, TaskStatus


class NotificationLevel(IntEnum):
    SUCCESS = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class Colors(str, Enum):
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"
    RESET = "reset"
    BRIGHT_BLACK = "bright_black"
    BRIGHT_RED = "bright_red"
    BRIGHT_GREEN = "bright_green"
    BRIGHT_YELLOW = "bright_yellow"
    BRIGHT_BLUE = "bright_blue"
    BRIGHT_MAGENTA = "bright_magenta"
    BRIGHT_CYAN = "bright_cyan"
    BRIGHT_WHITE = "bright_white"


def date(date: datetime.date) -> str:
    return date.strftime("%a, %d %B %Y")


def task_status(status: TaskStatus):
    symbol = "⬢"
    color = {
        TaskStatus.TODO: Colors.WHITE,
        TaskStatus.BLOCKED: Colors.BRIGHT_YELLOW,
        TaskStatus.DELETED: Colors.RED,
        TaskStatus.DONE: Colors.GREEN,
    }.get(status, Colors.BLACK)

    return click.style(symbol, fg=color)


def prompt(text: str):
    symbol = click.style("?", fg=Colors.BRIGHT_GREEN)
    return f"{symbol} {text}"


def task(task: Task, show_details: bool = False, show_prefix: bool = False) -> str:
    empty_details = "No details provided ..."

    title_style = {
        TaskStatus.DELETED: {"fg": Colors.BRIGHT_BLACK},
        TaskStatus.DONE: {"strikethrough": True},
    }.get(task.status, {})

    title = click.style(task.title, **title_style)  # type: ignore
    details = "⊕" if task.details else "◌"
    prefix = f"Task: #{task.id} " if show_prefix else ""

    headline = f"{prefix}{task_status(task.status)} {title}"

    if show_details:
        return f"{headline}\n{task.details or empty_details}"

    return f"{headline} {details}"


def tasks(tasks: List[Task], newline: bool = False) -> str:
    headers = ["#", "tasks"]
    suffix = "\n" if newline else ""
    lines = [[t.id, task(t)] for t in tasks]

    return f"{tabulate(lines, headers)} {suffix}"


def notification(text: str, event: str, status: NotificationLevel) -> str:
    symbol, color = {
        NotificationLevel.SUCCESS: ("✔", Colors.BRIGHT_GREEN),
        NotificationLevel.INFO: ("ℹ", Colors.BRIGHT_CYAN),
        NotificationLevel.WARNING: ("▼", Colors.BRIGHT_YELLOW),
        NotificationLevel.ERROR: ("✘", Colors.BRIGHT_RED),
    }.get(status, (">", Colors.BRIGHT_WHITE))
    prefix = click.style(f"{symbol}({event})", fg=color)

    return f"{prefix} {text}"
