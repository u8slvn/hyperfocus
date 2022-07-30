from __future__ import annotations

import click

from hyperfocus.console.commands._task import UpdateTasksCmd
from hyperfocus.database.models import TaskStatus
from hyperfocus.session import Session, get_current_session


@click.command(help="Delete given task")
@click.argument("task_ids", metavar="<id>", required=False, nargs=-1, type=click.INT)
def delete(task_ids: tuple[int, ...]) -> Session:
    session = get_current_session()
    UpdateTasksCmd(session).execute(
        task_ids=task_ids, status=TaskStatus.DELETED, text="Delete task"
    )

    return session
