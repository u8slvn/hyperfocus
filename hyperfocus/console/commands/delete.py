from __future__ import annotations

import click

from hyperfocus.console.commands._task import update_tasks
from hyperfocus.database.models import TaskStatus
from hyperfocus.session import get_current_session


@click.command(help="Delete given task")
@click.argument("task_ids", metavar="<id>", required=False, nargs=-1, type=click.INT)
def delete(task_ids: tuple[int, ...]) -> None:
    session = get_current_session()

    update_tasks(
        session=session,
        task_ids=task_ids,
        status=TaskStatus.DELETED,
        prompt_text="Delete task",
    )
