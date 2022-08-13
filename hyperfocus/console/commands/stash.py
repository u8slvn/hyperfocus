from __future__ import annotations

import click

from hyperfocus.console.commands._task import show_tasks
from hyperfocus.console.exceptions import TaskError
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import formatter, printer, prompt
from hyperfocus.termui.components import SuccessNotification


@click.group(help="Stash task")
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
                f"{formatter.task(task=task, show_prefix=True)} stashed."
            )
        )


# @stash.command(help="Pop stashed task")
# @click.argument(
#     "task_ids",
#     metavar="<id>",
#     nargs=-1,
#     type=click.INT,
# )
# def pop(task_ids: tuple[int, ...] | None) -> None:
#     printer.echo(f"hello {task_ids}")
