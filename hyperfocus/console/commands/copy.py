from __future__ import annotations

import click

from hyperfocus.console.commands.task import CopyTaskDetailsCmd
from hyperfocus.session import Session, get_current_session


@click.command(help="Copy task details into clipboard")
@click.argument("task_id", metavar="<id>", required=False, type=click.INT)
def copy(task_id: int | None) -> Session:
    session = get_current_session()
    CopyTaskDetailsCmd(session).execute(task_id=task_id)

    return session
