from __future__ import annotations

import click

from hyperfocus.console.core.arguments import NotRequiredIf
from hyperfocus.console.core.options import NotRequired
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import formatter
from hyperfocus.termui import printer
from hyperfocus.termui import style
from hyperfocus.termui.components import SuccessNotification


@click.command(help="Add task to current working day")
@click.argument(
    "title",
    cls=NotRequiredIf,
    not_required_if=["bulk"],
    metavar="<title>",
    type=click.STRING,
)
@click.option(
    "-d",
    "--details",
    "details",
    cls=NotRequired,
    not_required=["bulk"],
    default="",
    type=click.STRING,
    help="add task details",
)
@click.option(
    "-b",
    "--bulk",
    "bulk",
    cls=NotRequired,
    not_required=["title", "details"],
    is_flag=True,
    help="add multiple tasks",
)
def add(title: str, details: str, bulk: bool) -> None:
    session = get_current_session()

    tasks: list[tuple[str, str | None]] = []

    if bulk is True:
        bulk_input = click.edit() or ""
        task_titles = [line.strip() for line in bulk_input.splitlines() if line.strip()]
        tasks.extend((title, "") for title in task_titles)
    else:
        details_content = click.edit() if details == "-" else details
        tasks.append((title, details_content))

    for title, details_content in tasks:
        task = session.daily_tracker.create_task(title=title, details=details_content)
        printer.echo(
            SuccessNotification(
                text=(
                    f"{formatter.task(task=task, show_prefix=True)} "
                    f"[{style.INFO}]created[/]"
                )
            )
        )
