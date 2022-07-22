from __future__ import annotations

import sys

import click

from hyperfocus import __app_name__, __version__
from hyperfocus.console.commands.add import add
from hyperfocus.console.commands.config import config
from hyperfocus.console.commands.copy import copy
from hyperfocus.console.commands.delete import delete
from hyperfocus.console.commands.done import done
from hyperfocus.console.commands.init import init
from hyperfocus.console.commands.new_day import (
    CheckUnfinishedTasksCmd,
    NewDayCmd,
    ReviewUnfinishedTasksCmd,
)
from hyperfocus.console.commands.reset import reset
from hyperfocus.console.commands.show import show
from hyperfocus.console.commands.status import status
from hyperfocus.console.commands.task import ListTaskCmd
from hyperfocus.console.core.decorators import hyperfocus
from hyperfocus.session import Session


@hyperfocus(invoke_without_command=True, help="Minimalist task manager")
@click.version_option(
    version=__version__, prog_name=__app_name__, help="Show the version"
)
@click.pass_context
def hyf(ctx: click.Context) -> None:
    if ctx.invoked_subcommand in ["init"] or "--help" in sys.argv[1:]:
        return

    session = Session()
    session.bind_context(ctx=ctx)

    NewDayCmd(session).execute()
    if ctx.invoked_subcommand is not None:
        CheckUnfinishedTasksCmd(session).execute()
        return

    ReviewUnfinishedTasksCmd(session).execute()
    ListTaskCmd(session).execute()


@hyf.result_callback()
def process_session(session: Session | None, **_):
    if session is None:
        return

    for callback_commands in session.callback_commands:
        callback_commands()


hyf.add_commands(
    [
        add,
        config,
        copy,
        delete,
        done,
        init,
        reset,
        show,
        status,
    ]
)
