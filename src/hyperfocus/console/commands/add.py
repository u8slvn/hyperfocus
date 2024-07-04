from __future__ import annotations

import click

from hyperfocus.services.session import get_current_session
from hyperfocus.termui import formatter
from hyperfocus.termui import printer
from hyperfocus.termui.components import SuccessNotification


@click.command(help="Add task to current working day")
@click.argument("title", metavar="<title>", type=click.STRING)
@click.option(
    "-d", "--details", "details", default="", type=click.STRING, help="add task details"
)
def add(title: str, details: str) -> None:
    session = get_current_session()

    details_content = click.edit() if details == "-" else details

    task = session.daily_tracker.create_task(title=title, details=details_content)
    printer.echo(
        SuccessNotification(
            text=f"{formatter.task(task=task, show_prefix=True)} created",
        )
    )
