from __future__ import annotations

import datetime
from enum import IntEnum, auto

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.termui import icons


PROGRESS_BAR_SIZE = 30


class NotificationLevel(IntEnum):
    SUCCESS = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


def date(date: datetime.date) -> str:
    return date.strftime("%a, %d %B %Y")


def prompt(text: str):
    return f"[chartreuse3]{icons.PROMPT}[/] {text}"


def task(task: Task, show_details: bool = False, show_prefix: bool = False) -> str:
    empty_details = "No details provided ..."

    title_style = {
        TaskStatus.DELETED: "[bright_black]{title}[/]",
        TaskStatus.DONE: "[strike]{title}[/]",
    }.get(task.status, "{title}")

    title = title_style.format(title=task.title)
    prefix = f"Task: #{str(task.id)} " if show_prefix else ""

    headline = f"{prefix}{task_status(task.status)} {title}"

    if show_details:
        return f"{headline}\n{task.details or empty_details}"

    return headline


def task_status(status: TaskStatus):
    color = {
        TaskStatus.TODO: "bright_white",
        TaskStatus.BLOCKED: "orange1",
        TaskStatus.DELETED: "deep_pink2",
        TaskStatus.DONE: "chartreuse3",
    }.get(status, "bright_black")

    return f"[{color}]{icons.TASK_STATUS}[/]"


def notification(text: str, event: str, status: NotificationLevel) -> str:
    color, icon = {
        NotificationLevel.SUCCESS: ("chartreuse3", icons.NOTIFICATION_SUCCESS),
        NotificationLevel.INFO: ("steel_blue1", icons.NOTIFICATION_INFO),
        NotificationLevel.WARNING: ("orange1", icons.NOTIFICATION_WARNING),
        NotificationLevel.ERROR: ("deep_pink2", icons.NOTIFICATION_ERROR),
    }.get(status, ("bright_white", icons.NOTIFICATION))
    prefix = f"[{color}]{icon}({event})[/]"

    return f"{prefix} {text}"


def progress_bar(tasks: list[Task]):
    done_tasks = list(filter(lambda task: task.status == TaskStatus.DONE, tasks))
    done_count = len(done_tasks)
    total_count = len(tasks)

    percent_done = done_count * 100 / total_count
    percent_todo = 100 - percent_done
    display_done_count = round((percent_done * PROGRESS_BAR_SIZE) / 100)
    display_todo_count = PROGRESS_BAR_SIZE - display_done_count

    return (
        f"[chartreuse3]{int(percent_done)}% ["
        f"{icons.PROGRESS_BAR * display_done_count}[/]"
        f"[bright_white]{icons.PROGRESS_BAR * display_todo_count}"
        f"] {int(percent_todo)}%[/]"
    )
