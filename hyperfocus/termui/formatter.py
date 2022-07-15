from __future__ import annotations

import datetime
from enum import Enum, IntEnum, auto

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.termui import icons


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
    }.get(status, ("bright_white", Colors.BRIGHT_WHITE))
    prefix = f"[{color}]{icon}({event})[/]"

    return f"{prefix} {text}"
