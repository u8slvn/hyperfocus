from __future__ import annotations

import click

from hyperfocus.services.session import get_current_session
from hyperfocus.termui import printer
from hyperfocus.termui.components import ProgressBar, TasksTable


@click.command(help="Show current working day status")
def status() -> None:
    session = get_current_session()

    tasks = session.daily_tracker.get_tasks()
    if tasks:
        printer.echo(TasksTable(tasks))
        printer.echo(ProgressBar(tasks))
    else:
        printer.echo("No tasks for today...")
