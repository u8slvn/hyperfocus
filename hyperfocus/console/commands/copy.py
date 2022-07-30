from __future__ import annotations

import click
import pyperclip

from hyperfocus.exceptions import HyperfocusExit, TaskError
from hyperfocus.session import get_current_session
from hyperfocus.termui import printer, prompt
from hyperfocus.termui.components import SuccessNotification, TasksTable


@click.command(help="Copy task details into clipboard")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def copy(task_id: int | None) -> None:
    session = get_current_session()

    if task_id is None:
        tasks = session.daily_tracker.get_tasks()

        if not tasks:
            printer.echo("No tasks for today...")
            raise HyperfocusExit()

        printer.echo(TasksTable(tasks))
        task_id = prompt.prompt("Copy task details", type=click.INT)

    task = session.daily_tracker.get_task(task_id)

    if not task:
        raise TaskError(f"Task {task_id} does not exist.")

    if not task.details:
        raise TaskError(f"Task {task_id} does not have details.")

    pyperclip.copy(task.details)
    printer.echo(SuccessNotification(f"Task {task_id} details copied to clipboard."))
