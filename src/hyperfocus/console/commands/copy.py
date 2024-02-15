from __future__ import annotations

import click
import pyperclip

from hyperfocus.console.commands._shortcodes import TaskCommands
from hyperfocus.console.exceptions import TaskError
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import printer
from hyperfocus.termui.components import SuccessNotification


@click.command(help="Copy task details into clipboard")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def copy(task_id: int | None) -> None:
    session = get_current_session()
    task_cmd = TaskCommands(session)

    if task_id is None:
        task_id = task_cmd.pick_task(prompt_text="Copy task details")
    task = task_cmd.get_task(task_id=task_id)

    if not task.details:
        raise TaskError(f"Task {task.id} does not have details.")

    pyperclip.copy(task.details)
    printer.echo(SuccessNotification(f"Task {task_id} details copied to clipboard."))
