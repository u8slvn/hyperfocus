from __future__ import annotations

import click

from hyperfocus.services.history import History
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import formatter, printer


@click.command(help="Show tasks history")
def log() -> None:
    session = get_current_session()

    history = History(session.daily_tracker)

    printer.pager_echo(formatter.history(history))
