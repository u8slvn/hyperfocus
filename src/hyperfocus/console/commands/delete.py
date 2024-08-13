from __future__ import annotations

import click

from hyperfocus.console.commands._shortcodes import TaskCommands
from hyperfocus.database.models import TaskStatus
from hyperfocus.services.session import get_current_session
from hyperfocus.termui import formatter
from hyperfocus.termui import printer
from hyperfocus.termui import style
from hyperfocus.termui.components import SuccessNotification


@click.command(help="Delete given task")
@click.argument("task_ids", metavar="<id>", required=False, nargs=-1, type=click.INT)
@click.option("-f", "--force", is_flag=True, help="Hard delete")
def delete(task_ids: tuple[int, ...], force: bool) -> None:
    session = get_current_session()
    task_cmd = TaskCommands(session)

    if force:
        if not task_ids:
            task_id = task_cmd.pick_task(prompt_text="Force delete task")
            task_ids = (task_id,)

        for task_id in task_ids:
            task = task_cmd.get_task(task_id=task_id)
            session.daily_tracker.delete_task(task)

            task.status = TaskStatus.DELETED
            printer.echo(
                SuccessNotification(
                    f"{formatter.task(task=task, show_prefix=True)} "
                    f"[{style.INFO}]force deleted[/]."
                )
            )
    else:
        tasks = task_cmd.get_tasks(task_ids=task_ids, prompt_text="Delete task")
        task_cmd.update_tasks_status(tasks=tasks, status=TaskStatus.DELETED)
