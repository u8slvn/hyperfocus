from __future__ import annotations

import click

from hyperfocus.console.commands._shortcodes import TaskCommands
from hyperfocus.console.core.group import DefaultCommandGroup
from hyperfocus.console.exceptions import HyperfocusExit, TaskError
from hyperfocus.services.session import get_current_session
from hyperfocus.services.stash_box import StashBox
from hyperfocus.termui import formatter, printer, prompt
from hyperfocus.termui.components import SuccessNotification, TasksTable


@click.group(cls=DefaultCommandGroup, help="Task stash box")
def stash() -> None:
    ...


@stash.command(default_command=True, help="Stash task")
@click.argument(
    "task_ids",
    metavar="<id>",
    nargs=-1,
    type=click.INT,
)
def push(task_ids: tuple[int, ...] | None) -> None:
    session = get_current_session()
    task_cmd = TaskCommands(session)
    stash_box = StashBox(session.daily_tracker)

    if not task_ids:
        task_id = task_cmd.pick_task(prompt_text="Stash task")
        task_ids = (task_id,)

    for task_id in task_ids:
        task = session.daily_tracker.get_task(task_id)
        if not task:
            raise TaskError(f"Task {task_id} does not exist.")

        stash_box.add(task)

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
    stash_box = StashBox(session.daily_tracker)

    if not task_ids:
        stashed_tasks = stash_box.get_tasks()
        if not stashed_tasks:
            printer.echo("No tasks in stash box...")
            raise HyperfocusExit()

        printer.echo(TasksTable(stashed_tasks))

        task_id = prompt.prompt("Stash task", type=click.INT)
        task_ids = (task_id,)

    for i, task_id in enumerate(task_ids):
        # Decrease task_id because pop remove tasks from task from stash box
        task = stash_box.pop(task_id - i)

        printer.echo(
            SuccessNotification(
                f"{formatter.stashed_task(task_id, task=task)} added from stash box."
            )
        )


@stash.command(help="List stashed task")
def list() -> None:
    session = get_current_session()
    stash_box = StashBox(session.daily_tracker)

    stashed_tasks = stash_box.get_tasks()

    if not stashed_tasks:
        printer.echo("No tasks in stash box...")
        raise HyperfocusExit()

    printer.echo(TasksTable(stashed_tasks))


@stash.command(help="Clear stashed task")
def clear() -> None:
    session = get_current_session()
    stash_box = StashBox(session.daily_tracker)

    stash_box.clear()

    printer.echo(SuccessNotification("Stash box cleared."))


@stash.command(help="Pop all tasks in stash box")
def apply() -> None:
    session = get_current_session()
    stash_box = StashBox(session.daily_tracker)

    stash_box.apply()

    printer.echo(SuccessNotification("All tasks in stash box added for today."))
