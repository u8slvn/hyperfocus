from typing import List, Optional

import click

from hyperfocus import formatter, printer
from hyperfocus.exceptions import TaskError
from hyperfocus.models import Task as TaskModel, TaskStatus
from hyperfocus.session import Session


class CLIHelper:
    def __init__(self, session: Session):
        self._session = session


class Task(CLIHelper):
    def check_task_id_or_ask(
        self, task_id: int, text: str, exclude: Optional[List[TaskStatus]] = None
    ) -> int:
        if task_id:
            return task_id

        exclude = exclude or []
        self.show_tasks(newline=True, exclude=exclude)

        return printer.ask(text, type=int)

    def show_tasks(
        self, exclude: Optional[List[TaskStatus]] = None, newline=False
    ) -> None:
        exclude = exclude or []
        tasks = self._session.daily_tracker.get_tasks(exclude=exclude)
        if not tasks:
            printer.echo("No tasks for today...")
            raise click.exceptions.Exit
        printer.tasks(tasks=tasks, newline=newline)

    def get_task(self, task_id: int) -> TaskModel:
        task = self._session.daily_tracker.get_task(task_id=task_id)
        if not task:
            raise TaskError(f"Task {task_id} does not exist", event="not found")

        return task

    def update_task(self, task_id: int, status: TaskStatus, text: str):
        task_id = self.check_task_id_or_ask(
            task_id=task_id, text=text, exclude=[status]
        )

        task = self.get_task(task_id=task_id)
        if task.status == status.value:
            printer.warning(
                text=formatter.task(task=task, show_prefix=True),
                event="no change",
            )
            raise click.exceptions.Exit

        task.status = status
        self._session.daily_tracker.update_task(task=task, status=status)
        printer.success(
            text=formatter.task(task=task, show_prefix=True),
            event="updated",
        )


class NewDay(CLIHelper):
    def manage_new_day(self):
        if not self._session.is_a_new_day():
            return

        printer.echo(f"✨ {formatter.date(date=self._session.date)}")
        printer.echo("✨ A new day starts, good luck!\n")

        self._review_unfinished_tasks()

    def _review_unfinished_tasks(self):
        prev_day = self._session.past_tracker.get_previous_day()
        finished_status = [TaskStatus.DELETED, TaskStatus.DONE]
        if not (tasks := prev_day.get_tasks(exclude=finished_status)):
            return

        printer.echo(f"Unfinished task(s) from {formatter.date(date=prev_day.date)}:")
        printer.tasks(tasks=tasks, newline=True)
        if not printer.confirm(
            f"Review {len(tasks)} unfinished task(s)",
            default=True,
        ):
            return

        for task in tasks:
            if printer.confirm(f'Take back task "{task.title}" for today'):
                self._session.daily_tracker.add_task(
                    title=task.title, details=task.details
                )
        printer.echo("")  # Empty line for design
