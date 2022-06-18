import datetime
from enum import IntEnum, auto
from typing import List

import click
from tabulate import tabulate

from hyperfocus.models import Task, TaskStatus


class NotificationStatus(IntEnum):
    SUCCESS = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class Formatter:
    @staticmethod
    def date(date: datetime.date) -> str:
        return date.strftime("%a, %d %B %Y")

    @staticmethod
    def task_status(status: TaskStatus):
        symbol = "⬢"
        color = {
            TaskStatus.TODO: "white",
            TaskStatus.BLOCKED: "bright_yellow",
            TaskStatus.DELETED: "red",
            TaskStatus.DONE: "green",
        }.get(status, "black")

        return click.style(symbol, fg=color)

    @staticmethod
    def prompt(text: str):
        symbol = click.style("?", fg="bright_green")
        return f"{symbol} {text}"

    @classmethod
    def task(
        cls, task: Task, show_details: bool = False, show_prefix: bool = False
    ) -> str:
        empty_details = "No details provided ..."

        title_style = {
            TaskStatus.DELETED: {"fg": "bright_black"},
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
    def notification(cls, text: str, action: str, status: NotificationStatus):
        symbol, color = {
            NotificationStatus.SUCCESS: ("✔", "bright_green"),
            NotificationStatus.INFO: ("ℹ", "bright_cyan"),
            NotificationStatus.WARNING: ("▼", "bright_yellow"),
            NotificationStatus.ERROR: ("✘", "bright_red"),
        }.get(status, (">", "bright_white"))
        prefix = click.style(f"{symbol}({action})", fg=color)

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
        cls.echo(formatted_task)

    @classmethod
    def tasks(cls, tasks: List[Task], newline: bool = False):
        formatted_tasks = Formatter.tasks(tasks=tasks, newline=newline)
        cls.echo(formatted_tasks)

    @classmethod
    def notification(cls, text: str, action: str, status: NotificationStatus):
        formatted_notification = Formatter.notification(
            text=text, action=action, status=status
        )
        cls.echo(formatted_notification)
