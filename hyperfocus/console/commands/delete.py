from __future__ import annotations

import click

from hyperfocus.console.commands._task import get_task, pick_task, update_tasks
from hyperfocus.database.models import TaskStatus
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import formatter, printer
from hyperfocus.termui.components import SuccessNotification


@click.command(help="Delete given task")
@click.argument("task_ids", metavar="<id>", required=False, nargs=-1, type=click.INT)
@click.option("-f", "--force", is_flag=True, help="Hard delete")
def delete(task_ids: tuple[int, ...], force: bool) -> None:
    session = get_current_session()

    if force:
        if not task_ids:
            task_id = pick_task(session=session, prompt_text="Force delete task")
            task_ids = (task_id,)

        for task_id in task_ids:
            task = get_task(session=session, task_id=task_id)
            session.daily_tracker.delete_task(task)

            task.status = TaskStatus.DELETED
            printer.echo(
                SuccessNotification(
                    f"{formatter.task(task=task, show_prefix=True)} force deleted."
                )
            )
    else:
        update_tasks(
            session=session,
            task_ids=task_ids,
            status=TaskStatus.DELETED,
            prompt_text="Delete task",
        )
