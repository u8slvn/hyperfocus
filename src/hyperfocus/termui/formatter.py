from __future__ import annotations

import datetime

from typing import Generator

from hyperfocus.database.models import Task
from hyperfocus.database.models import TaskStatus
from hyperfocus.services.history import History
from hyperfocus.termui import icons
from hyperfocus.termui import style


def date(date: datetime.date) -> str:
    return date.strftime("%a, %d %B %Y")


def date_with_time(date: datetime.datetime) -> str:
    return date.strftime("%a, %d %B %Y at %H:%M:%S")


def task(task: Task, show_prefix: bool = False) -> str:
    title_style = {
        TaskStatus.DELETED: f"[{style.DELETED_TASK}]{{title}}[/]",
        TaskStatus.DONE: f"[{style.DONE_TASK}]{{title}}[/]",
    }.get(task.status, "{title}")

    title = title_style.format(title=task.title)
    prefix = f"Task: #{task.id!s} " if show_prefix else ""

    return f"{prefix}{task_status(task.status)} {title}"


def task_details(value: str | None) -> str:
    """Format task details.

    If no details, return an ellipsis, if details contains a single line, otherwise
    indent each line with an icon prefix and start with a newline.
    """
    if not value:
        return icons.EMPTY_DETAILS

    lines = value.splitlines()
    if len(lines) > 1:
        start, *middle, end = lines

        start = f"{icons.MULTILINES_DETAILS_START} {start}"
        middle = [f"{icons.MULTILINES_DETAILS_MIDDLE} {line}" for line in middle]
        end = f"{icons.MULTILINES_DETAILS_END} {end}"

        return "\n" + "\n".join([start, *middle, end])
    else:
        return value


def stashed_task(old_task_id: int, task: Task) -> str:
    # TODO: find a way to merge with classic task formatter.
    prefix = f"Task: #{old_task_id!s} "
    return f"{prefix}{task_status(task.status)} {task.title}"


def task_status(status: TaskStatus) -> str:
    color = {
        TaskStatus.TODO: style.DEFAULT,
        TaskStatus.DELETED: style.ERROR,
        TaskStatus.DONE: style.SUCCESS,
        TaskStatus.STASHED: style.STASHED,
    }.get(status, style.UNKNOWN)

    return f"[{color}]{icons.TASK_STATUS}[/]"


def config(config: dict[str, str]) -> str:
    return "\n".join([f"[{style.INFO}]{k}[/] = {v}" for k, v in config.items()])


def history(history: History) -> Generator[str, None, None]:
    for last_element, data in history():
        if isinstance(data, Task):
            icon = icons.HISTORY_END_NODE if last_element else icons.HISTORY_NODE
            end = "\n\n" if last_element else "\n"
            yield f"{icon} {(task(data))}{end}"

        if isinstance(data, datetime.date):
            yield f"{icons.LIST} {date(data)}\n"
