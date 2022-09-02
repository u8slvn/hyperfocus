from __future__ import annotations

from typing import TYPE_CHECKING

import click

from hyperfocus.console.exceptions import HyperfocusExit, TaskError
from hyperfocus.database.models import TaskStatus
from hyperfocus.termui import formatter, printer, prompt, style
from hyperfocus.termui.components import (
    SuccessNotification,
    TasksTable,
    WarningNotification,
)


if TYPE_CHECKING:
    from hyperfocus.database.models import Task
    from hyperfocus.services.daily_tracker import DailyTracker
    from hyperfocus.services.session import Session


class TaskCommands:
    def __init__(self, session: Session) -> None:
        self.session = session

    def show_tasks(self):
        tasks = self.session.daily_tracker.get_tasks()

        if not tasks:
            printer.echo("No tasks for today...")
            raise HyperfocusExit()

        printer.echo(TasksTable(tasks))

    def pick_task(self, prompt_text: str) -> int:
        self.show_tasks()
        return prompt.prompt(prompt_text, type=click.INT)

    def get_task(self, task_id: int) -> Task:
        task = self.session.daily_tracker.get_task(task_id)
        if not task:
            raise TaskError(f"Task {task_id} does not exist.")

        return task

    def update_tasks(
        self, task_ids: tuple[int, ...], status: TaskStatus, prompt_text: str
    ) -> None:
        if not task_ids:
            task_id = self.pick_task(prompt_text=prompt_text)
            task_ids = (task_id,)

        for task_id in task_ids:
            task = self.get_task(task_id=task_id)

            if task.status == status.value:
                printer.echo(
                    WarningNotification(
                        f"{formatter.task(task=task, show_prefix=True)} unchanged."
                    )
                )
                continue

            self.session.daily_tracker.update_task(task=task, status=status)

            text_suffix = "reset" if status == TaskStatus.TODO else status.name.lower()
            printer.echo(
                SuccessNotification(
                    f"{formatter.task(task=task, show_prefix=True)} {text_suffix}."
                )
            )


class TasksReviewer:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _get_unfinished_task(previous_day: DailyTracker):
        unfinished_tasks = []
        if previous_day and not previous_day.is_locked():
            finished_status = [TaskStatus.DELETED, TaskStatus.DONE]
            unfinished_tasks = previous_day.get_tasks(exclude=finished_status)

        return unfinished_tasks

    def show_review_reminder(self):
        previous_day = self.session.daily_tracker.get_previous_day()
        unfinished_tasks = self._get_unfinished_task(previous_day)

        if len(unfinished_tasks) > 0 and previous_day:
            printer.banner(
                f"You have {len(unfinished_tasks)} unfinished task(s) from "
                f"{formatter.date(date=previous_day.date)}, run 'hyf' "
                f"to review."
            )

    def review_tasks(self):
        previous_day = self.session.daily_tracker.get_previous_day()
        unfinished_tasks = self._get_unfinished_task(previous_day)

        if len(unfinished_tasks) > 0 and previous_day:
            if prompt.confirm(
                f"Review [{style.INFO}]{len(unfinished_tasks)}[/] unfinished task(s) "
                f"from {formatter.date(date=previous_day.date)}",
                default=True,
            ):
                for task in unfinished_tasks:
                    if prompt.confirm(f'Continue "[{style.INFO}]{task.title}[/]"'):
                        self.session.daily_tracker.copy_task(task)

        if previous_day:
            previous_day.locked()
