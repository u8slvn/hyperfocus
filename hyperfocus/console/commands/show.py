from __future__ import annotations

import click

from hyperfocus.console.commands._task import get_task, pick_task
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import printer
from hyperfocus.termui.components import TaskDetails


@click.command(help="Show task details")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def show(task_id: int | None) -> None:
    session = get_current_session()

    if task_id is None:
        task_id = pick_task(session=session, prompt_text="Show task details")
    task = get_task(session=session, task_id=task_id)

    printer.echo(TaskDetails(task))
