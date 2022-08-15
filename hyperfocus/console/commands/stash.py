from __future__ import annotations

import click

from hyperfocus.console.commands._task import show_tasks
from hyperfocus.console.exceptions import HyperfocusExit, TaskError
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import formatter, printer, prompt
from hyperfocus.termui.components import SuccessNotification, TasksTable


@click.group(help="Task stash box")
def stash() -> None:
    ...


@stash.command(help="Stash task")
@click.argument(
    "task_ids",
    metavar="<id>",
    nargs=-1,
    type=click.INT,
)
def add(task_ids: tuple[int, ...] | None) -> None:
    session = get_current_session()

    if not task_ids:
        show_tasks(session)

        task_id = prompt.prompt("Stash task", type=click.INT)
        task_ids = (task_id,)

    for task_id in task_ids:
        task = session.daily_tracker.get_task(task_id)
        if not task:
            raise TaskError(f"Task {task_id} does not exist.")

        session.stash_box.add(task)

        printer.echo(
            SuccessNotification(
                f"{formatter.stashed_task(task_id, task=task)} stashed."
            )
        )


@stash.command(help="Pop stashed task")
@click.argument(
    "task_ids",
    metavar="<id>",
    nargs=-1,
    type=click.INT,
)
def pop(task_ids: tuple[int, ...] | None) -> None:
    session = get_current_session()

    if not task_ids:
        stashed_tasks = session.stash_box.get_tasks()
        if not stashed_tasks:
            printer.echo("No tasks in stash box...")
            raise HyperfocusExit()

        printer.echo(TasksTable(stashed_tasks))

        task_id = prompt.prompt("Stash task", type=click.INT)
        task_ids = (task_id,)

    for i, task_id in enumerate(task_ids):
        # Decrease task_id because pop remove tasks from task from stash box
        task = session.stash_box.pop(task_id - i)

        printer.echo(
            SuccessNotification(
                f"{formatter.stashed_task(task_id, task=task)} added from stash box."
            )
        )


@stash.command(help="List stashed task")
def list() -> None:
    session = get_current_session()

    stashed_tasks = session.stash_box.get_tasks()

    if not stashed_tasks:
        printer.echo("No tasks in stash box...")
        raise HyperfocusExit()

    printer.echo(TasksTable(stashed_tasks))
