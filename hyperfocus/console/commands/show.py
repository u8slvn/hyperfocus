from __future__ import annotations

import click

from hyperfocus.console.commands.task import ShowTaskCmd
from hyperfocus.session import Session, get_current_session


@click.command(help="Show task details")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def show(task_id: int | None) -> Session:
    session = get_current_session()
    ShowTaskCmd(session).execute(task_id=task_id)

    return session
