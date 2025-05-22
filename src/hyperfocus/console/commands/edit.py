from __future__ import annotations

import click

from hyperfocus.console.commands._shortcodes import TaskCommands
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import formatter
from hyperfocus.termui import printer
from hyperfocus.termui import style
from hyperfocus.termui.components import SuccessNotification
from hyperfocus.termui.components import WarningNotification


@click.command(help="Edit task from current working day")
@click.argument("task_ids", metavar="<id>", required=False, nargs=-1, type=click.INT)
@click.option(
    "-t",
    "--title",
    "title",
    is_flag=True,
    help="Edit task title.",
)
@click.option(
    "-d",
    "--details",
    "details",
    is_flag=True,
    help="Edit task details.",
)
def edit(task_ids: tuple[int, ...], title: bool, details: bool) -> None:
    session = get_current_session()
    task_cmd = TaskCommands(session)

    if not any([title, details]):
        title = details = True

    tasks = task_cmd.get_tasks(task_ids=task_ids, prompt_text="Edit task(s)")
    for task in tasks:
        edited = False  # Flag to check if task was edited

        if title:
            edited = (
                task_cmd.edit_task(task=task, field="title", splitlines=True) or edited
            )

        if details:
            edited = task_cmd.edit_task(task=task, field="details") or edited

        if edited is False:
            printer.echo(
                WarningNotification(
                    f"{formatter.task(task=task, show_prefix=True)} "
                    f"[{style.INFO}]unchanged[/]."
                )
            )
            continue

        session.daily_tracker.update_task(task=task)
        printer.echo(
            SuccessNotification(
                text=(
                    f"{formatter.task(task=task, show_prefix=True)} "
                    f"[{style.INFO}]edited[/]."
                )
            )
        )
