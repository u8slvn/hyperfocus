from __future__ import annotations

import click

from hyperfocus.exceptions import HyperfocusExit, TaskError
from hyperfocus.session import get_current_session
from hyperfocus.termui import printer, prompt
from hyperfocus.termui.components import TaskDetails, TasksTable


@click.command(help="Show task details")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def show(task_id: int | None) -> None:
    session = get_current_session()

    if task_id is None:
        tasks = session.daily_tracker.get_tasks()

        if not tasks:
            printer.echo("No tasks for today...")
            raise HyperfocusExit()

        printer.echo(TasksTable(tasks))
        task_id = prompt.prompt("Show task details", type=click.INT)

    task = session.daily_tracker.get_task(task_id)

    if not task:
        raise TaskError(f"Task {task_id} does not exist.")

    printer.echo(TaskDetails(task))
