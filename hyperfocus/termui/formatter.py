from __future__ import annotations

import datetime
from enum import IntEnum, auto

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.termui import icons, style


PROGRESS_BAR_SIZE = 30


class NotificationLevel(IntEnum):
    SUCCESS = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


def date(date: datetime.date) -> str:
    return date.strftime("%a, %d %B %Y")


def date_with_time(date: datetime.datetime) -> str:
    return date.strftime("%a, %d %B %Y at %H:%M:%S")


def prompt(text: str):
    return f"[{style.SUCCESS}]{icons.PROMPT}[/] {text}"


def task(task: Task, show_details: bool = False, show_prefix: bool = False) -> str:
    empty_details = "No details provided ..."

    title_style = {
        TaskStatus.DELETED: f"[{style.DELETED_TASK}]{{title}}[/]",
        TaskStatus.DONE: f"[{style.DONE_TASK}]{{title}}[/]",
    }.get(task.status, "{title}")

    title = title_style.format(title=task.title)
    prefix = f"Task: #{str(task.id)} " if show_prefix else ""

    headline = f"{prefix}{task_status(task.status)} {title}"

    if show_details:
        return f"{headline}\n{task.details or empty_details}"

    return headline


def task_details(task: Task) -> str:
    task_info = {
        "Task": f"#{task.id}",
        "Status": (
            f"{task_status(TaskStatus(task.status))} "
            f"{TaskStatus(task.status).name.title()}"
        ),
        "Title": task.title,
        "Details": task.details or "...",
        "History": "",
    }
    full_details = []
    for info, value in task_info.items():
        full_details.append(f"[{style.INFO}]{info}[/][{style.LIST_POINT}]:[/] {value}")

    return "\n".join(full_details) + f"\n{task_history(task)}"


def task_history(task: Task) -> str:
    bullet_point = f" [{style.LIST_POINT}]{icons.BULLET_POINT}[/] "
    history = [f"{bullet_point}{date_with_time(task.created_at)} - add task"]
    while True:
        task = task.parent_task
        if task is None:
            break
        step = f"{bullet_point}{date_with_time(task.created_at)} - recover task"
        history.append(step)
    history[-1] = history[-1].replace("recover task", "initial task creation")
    return "\n".join(history)


def task_status(status: TaskStatus) -> str:
    color = {
        TaskStatus.TODO: style.DEFAULT,
        TaskStatus.DELETED: style.ERROR,
        TaskStatus.DONE: style.SUCCESS,
    }.get(status, style.UNKNOWN)

    return f"[{color}]{icons.TASK_STATUS}[/]"


def notification(text: str, event: str, status: NotificationLevel) -> str:
    color, icon = {
        NotificationLevel.SUCCESS: (style.SUCCESS, icons.NOTIFICATION_SUCCESS),
        NotificationLevel.INFO: (style.INFO, icons.NOTIFICATION_INFO),
        NotificationLevel.WARNING: (style.WARNING, icons.NOTIFICATION_WARNING),
        NotificationLevel.ERROR: (style.ERROR, icons.NOTIFICATION_ERROR),
    }.get(status, (style.DEFAULT, icons.NOTIFICATION))
    prefix = f"[{color}]{icon}({event})[/]"

    return f"{prefix} {text}"


def progress_bar(tasks: list[Task]) -> str:
    done_tasks = list(filter(lambda task: task.status == TaskStatus.DONE, tasks))
    todo_tasks = list(filter(lambda task: task.status == TaskStatus.TODO, tasks))
    done_count = len(done_tasks)
    total_count = len(todo_tasks) + done_count

    percent_done = done_count * 100 / total_count
    percent_todo = 100 - percent_done
    display_done_count = round((percent_done * PROGRESS_BAR_SIZE) / 100)
    display_todo_count = PROGRESS_BAR_SIZE - display_done_count

    return (
        f"[{style.SUCCESS}]{int(percent_done)}% ["
        f"{icons.PROGRESS_BAR * display_done_count}[/]"
        f"[{style.DEFAULT}]{icons.PROGRESS_BAR * display_todo_count}"
        f"] {int(percent_todo)}%[/]"
    )
