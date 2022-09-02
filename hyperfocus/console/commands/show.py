from __future__ import annotations

import click

from hyperfocus.console.commands._shortcodes import TaskCommands
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import printer
from hyperfocus.termui.components import TaskDetails


@click.command(help="Show task details")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def show(task_id: int | None) -> None:
    session = get_current_session()
    task_cmd = TaskCommands(session)

    if task_id is None:
        task_id = task_cmd.pick_task(prompt_text="Show task details")
    task = task_cmd.get_task(task_id=task_id)

    printer.echo(TaskDetails(task))
