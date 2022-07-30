from __future__ import annotations

import click

from hyperfocus.console.commands._task import ListTaskCmd
from hyperfocus.session import Session, get_current_session


@click.command(help="Show current working day status")
def status() -> Session:
    session = get_current_session()
    ListTaskCmd(session).execute()

    return session
