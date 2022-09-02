from __future__ import annotations

import click

from hyperfocus.console.commands._shortcodes import TaskCommands
from hyperfocus.database.models import TaskStatus
from hyperfocus.services.session import get_current_session


@click.command(help="Reset task as todo")
@click.argument("task_ids", metavar="<id>", required=False, nargs=-1, type=int)
def reset(task_ids: tuple[int, ...]) -> None:
    session = get_current_session()
    task_cmd = TaskCommands(session)

    task_cmd.update_tasks(
        task_ids=task_ids,
        status=TaskStatus.TODO,
        prompt_text="Reset task",
    )
