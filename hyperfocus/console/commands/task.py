from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, cast

import click
import pyperclip

from hyperfocus.console.commands import SessionHyperfocusCommand
from hyperfocus.exceptions import HyperfocusExit, TaskError
from hyperfocus.termui import formatter, printer, prompt


if TYPE_CHECKING:
    from hyperfocus.database.models import Task, TaskStatus
    from hyperfocus.session import Session


class TaskCmd(SessionHyperfocusCommand, ABC):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    def check_task_id_or_ask(
        self, task_id: int | None, text: str, exclude: list[TaskStatus] | None = None
    ) -> int:
        if task_id:
            return task_id
        return self.ask_task_id(text=text, exclude=exclude)

    def ask_task_id(self, text: str, exclude: list[TaskStatus] | None = None) -> int:
        self.show_tasks(exclude=exclude)

        return prompt.prompt(text, type=click.INT)

    def show_tasks(
        self, exclude: list[TaskStatus] | None = None, progress_bar: bool = False
    ) -> None:
        exclude = exclude or []
        tasks = self._session.daily_tracker.get_tasks(exclude=exclude)

        if not tasks:
            printer.echo("No tasks for today...")
            raise HyperfocusExit()

        printer.tasks(tasks)
        if progress_bar:
            printer.progress_bar(tasks)

    def get_task(self, task_id: int) -> Task:
        task = self._session.daily_tracker.get_task(task_id=task_id)
        if not task:
            raise TaskError(f"Task {task_id} does not exist.")

        return task


class AddTaskCmd(TaskCmd):
    def execute(self, title: str, add_details: bool) -> None:
        details = prompt.prompt("Task details") if add_details else ""

        task = self._session.daily_tracker.add_task(title=title, details=details)
        printer.success(
            text=formatter.task(task=task, show_prefix=True),
            event="created",
        )


class UpdateTasksCmd(TaskCmd):
    def execute(self, task_ids: tuple[int, ...], status: TaskStatus, text: str) -> None:
        if not task_ids:
            task_id = self.ask_task_id(text=text, exclude=[status])
            task_ids = (task_id,)

        for task_id in task_ids:
            task = self.get_task(task_id=task_id)
            if task.status == status.value:
                printer.warning(
                    text=formatter.task(task=task, show_prefix=True),
                    event="no change",
                )
                continue

            self._session.daily_tracker.update_task(task=task, status=status)
            printer.success(
                text=formatter.task(task=task, show_prefix=True),
                event="updated",
            )


class ShowTaskCmd(TaskCmd):
    def execute(self, task_id: int | None) -> None:
        task_id = cast(int, task_id)
        task_id = self.check_task_id_or_ask(task_id=task_id, text="Show task")

        task = self.get_task(task_id=task_id)
        printer.task_details(task)


class ListTaskCmd(TaskCmd):
    def execute(self) -> None:
        self.show_tasks(progress_bar=True)


class CopyTaskDetailsCmd(TaskCmd):
    def execute(self, task_id: int | None) -> None:
        task_id = cast(int, task_id)
        task_id = self.check_task_id_or_ask(task_id=task_id, text="Copy task details")

        task = self.get_task(task_id=task_id)
        if not task.details:
            raise TaskError(f"Task {task_id} does not have details.")

        pyperclip.copy(task.details)
        printer.success(f"Task {task_id} details copied to clipboard.", event="success")
