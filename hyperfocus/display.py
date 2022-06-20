import datetime
from enum import Enum, IntEnum, auto
from typing import List

import click
from tabulate import tabulate

from hyperfocus.models import Task, TaskStatus


class NotificationStatus(IntEnum):
    SUCCESS = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class NotificationEvents(str, Enum):
    INIT = "init"
    NO_CHANGE = "no change"
    UPDATED = "updated"
    NOT_FOUND = "not found"
    CREATED = "created"


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


class Formatter:
    @staticmethod
    def date(date: datetime.date) -> str:
        return date.strftime("%a, %d %B %Y")

    @staticmethod
    def task_status(status: TaskStatus):
        symbol = "⬢"
        color = {
            TaskStatus.TODO: Colors.WHITE,
            TaskStatus.BLOCKED: Colors.BRIGHT_YELLOW,
            TaskStatus.DELETED: Colors.RED,
            TaskStatus.DONE: Colors.GREEN,
        }.get(status, Colors.BLACK)

        return click.style(symbol, fg=color)

    @staticmethod
    def prompt(text: str):
        symbol = click.style("?", fg=Colors.BRIGHT_GREEN)
        return f"{symbol} {text}"

    @classmethod
    def task(
        cls, task: Task, show_details: bool = False, show_prefix: bool = False
    ) -> str:
        empty_details = "No details provided ..."

        title_style = {
            TaskStatus.DELETED: {"fg": Colors.BRIGHT_BLACK},
            TaskStatus.DONE: {"strikethrough": True},
        }.get(task.status, {})

        title = click.style(task.title, **title_style)  # type: ignore
        details = "⊕" if task.details else "◌"
        prefix = f"Task: #{task.id} " if show_prefix else ""

        headline = f"{prefix}{cls.task_status(task.status)} {title}"

        if show_details:
            return f"{headline}\n{task.details or empty_details}"

        return f"{headline} {details}"

    @classmethod
    def tasks(cls, tasks: List[Task], newline: bool = False):
        headers = ["#", "tasks"]
        suffix = "\n" if newline else ""
        lines = [[t.id, cls.task(t)] for t in tasks]

        return f"{tabulate(lines, headers)} {suffix}"

    @classmethod
    def notification(cls, text: str, event: str, status: NotificationStatus):
        symbol, color = {
            NotificationStatus.SUCCESS: ("✔", Colors.BRIGHT_GREEN),
            NotificationStatus.INFO: ("ℹ", Colors.BRIGHT_CYAN),
            NotificationStatus.WARNING: ("▼", Colors.BRIGHT_YELLOW),
            NotificationStatus.ERROR: ("✘", Colors.BRIGHT_RED),
        }.get(status, (">", Colors.BRIGHT_WHITE))
        prefix = click.style(f"{symbol}({event})", fg=color)

        return f"{prefix} {text}"


class Printer:
    @staticmethod
    def echo(text: str):
        click.secho(text)

    @classmethod
    def task(cls, task: Task, show_details: bool = False, show_prefix: bool = False):
        formatted_task = Formatter.task(
            task=task, show_details=show_details, show_prefix=show_prefix
        )
        cls.echo(text=formatted_task)

    @classmethod
    def tasks(cls, tasks: List[Task], newline: bool = False):
        formatted_tasks = Formatter.tasks(tasks=tasks, newline=newline)
        cls.echo(text=formatted_tasks)

    @classmethod
    def notification(cls, text: str, event: str, status: NotificationStatus):
        formatted_notification = Formatter.notification(
            text=text, event=event, status=status
        )
        cls.echo(text=formatted_notification)

    @classmethod
    def ask(cls, text: str, *args, **kwargs) -> str:
        formatted_prompt = Formatter.prompt(text=text)
        return click.prompt(text=formatted_prompt, *args, **kwargs)
