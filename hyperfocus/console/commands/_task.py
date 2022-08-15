from __future__ import annotations

from typing import TYPE_CHECKING

import click

from hyperfocus.console.exceptions import HyperfocusExit, TaskError
from hyperfocus.database.models import TaskStatus
from hyperfocus.termui import formatter, printer, prompt
from hyperfocus.termui.components import (
    SuccessNotification,
    TasksTable,
    WarningNotification,
)


if TYPE_CHECKING:
    from hyperfocus.database.models import Task
    from hyperfocus.services.session import Session


def show_tasks(session: Session):
    tasks = session.daily_tracker.get_tasks()

    if not tasks:
        printer.echo("No tasks for today...")
        raise HyperfocusExit()

    printer.echo(TasksTable(tasks))


def pick_task(session: Session, prompt_text: str) -> int:
    show_tasks(session)
    return prompt.prompt(prompt_text, type=click.INT)


def get_task(session: Session, task_id: int) -> Task:
    task = session.daily_tracker.get_task(task_id)
    if not task:
        raise TaskError(f"Task {task_id} does not exist.")

    return task


def update_tasks(
    session: Session, task_ids: tuple[int, ...], status: TaskStatus, prompt_text: str
) -> None:
    if not task_ids:
        task_id = pick_task(session=session, prompt_text=prompt_text)
        task_ids = (task_id,)

    for task_id in task_ids:
        task = get_task(session=session, task_id=task_id)

        if task.status == status.value:
            printer.echo(
                WarningNotification(
                    f"{formatter.task(task=task, show_prefix=True)} unchanged."
                )
            )
            continue

        session.daily_tracker.update_task(task=task, status=status)

        text_suffix = "reset" if status == TaskStatus.TODO else status.name.lower()
        printer.echo(
            SuccessNotification(
                f"{formatter.task(task=task, show_prefix=True)} {text_suffix}."
            )
        )
