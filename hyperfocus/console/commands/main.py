from __future__ import annotations

import sys

import click

from hyperfocus import __app_name__, __version__
from hyperfocus.console.commands._shortcodes import TasksReviewer
from hyperfocus.console.commands.status import status
from hyperfocus.console.core.hyperfocus import hyperfocus
from hyperfocus.services.session import Session
from hyperfocus.termui import printer
from hyperfocus.termui.components import NewDay


@hyperfocus(invoke_without_command=True, help="Minimalist task manager")
@click.version_option(
    version=__version__, prog_name=__app_name__, help="Show the version"
)
@click.pass_context
def hyf(ctx: click.Context) -> None:
    if ctx.invoked_subcommand in ["init"] or "--help" in sys.argv[1:]:
        return

    session = Session.create()
    session.bind_context(ctx=ctx)

    if session.daily_tracker.is_a_new_day():
        printer.echo(NewDay(session.date))

    tasks_reviewer = TasksReviewer(session)

    if ctx.invoked_subcommand is not None:
        tasks_reviewer.show_review_reminder()
        return

    tasks_reviewer.review_tasks()

    ctx.invoke(status)
