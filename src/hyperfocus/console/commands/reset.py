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

    tasks = task_cmd.get_tasks(task_ids=task_ids, prompt_text="Reset task(s)")
    task_cmd.update_tasks_status(tasks=tasks, status=TaskStatus.TODO)
