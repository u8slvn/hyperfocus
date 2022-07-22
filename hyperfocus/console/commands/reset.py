from __future__ import annotations

import click

from hyperfocus.console.commands.hyf import hyf
from hyperfocus.console.commands.task import UpdateTasksCmd
from hyperfocus.database.models import TaskStatus
from hyperfocus.session import Session, get_current_session


@hyf.command(help="Reset task as todo")
@click.argument("task_ids", metavar="<id>", required=False, nargs=-1, type=int)
def reset(task_ids: tuple[int, ...]) -> Session:
    session = get_current_session()
    UpdateTasksCmd(session).execute(
        task_ids=task_ids, status=TaskStatus.TODO, text="Reset task"
    )

    return session
