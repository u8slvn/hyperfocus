from __future__ import annotations

import click

from hyperfocus.console.commands._task import get_task
from hyperfocus.session import get_current_session
from hyperfocus.termui import printer
from hyperfocus.termui.components import TaskDetails


@click.command(help="Show task details")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def show(task_id: int | None) -> None:
    session = get_current_session()

    task = get_task(session=session, task_id=task_id, prompt_text="Show task details")

    printer.echo(TaskDetails(task))
