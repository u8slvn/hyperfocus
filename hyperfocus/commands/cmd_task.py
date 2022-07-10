from __future__ import annotations

from typing import TYPE_CHECKING

import pyperclip

from hyperfocus import formatter
from hyperfocus.commands import SessionHyperfocusCommand, printer
from hyperfocus.exceptions import HyperfocusExit, TaskError
from hyperfocus.services import DailyTrackerService


if TYPE_CHECKING:
    from hyperfocus.database.models import Task, TaskStatus
    from hyperfocus.session import Session


class TaskCommand(SessionHyperfocusCommand):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)
        self._daily_tracker = DailyTrackerService.from_date(session.date)

    def check_task_id_or_ask(
        self, task_id: int | None, text: str, exclude: list[TaskStatus] | None = None
    ) -> int:
        if task_id:
            return task_id

        exclude = exclude or []
        self.show_tasks(newline=True, exclude=exclude)

        return printer.ask(text, type=int)

    def show_tasks(
        self, exclude: list[TaskStatus] | None = None, newline=False
    ) -> None:
        exclude = exclude or []
        tasks = self._daily_tracker.get_tasks(exclude=exclude)

        if not tasks:
            printer.echo("No tasks for today...")
            raise HyperfocusExit()

        printer.tasks(tasks=tasks, newline=newline)

    def get_task(self, task_id: int) -> Task:
        task = self._daily_tracker.get_task(task_id=task_id)
        if not task:
            raise TaskError(f"Task {task_id} does not exist.")

        return task

    def add_task(self, title: str, details: str) -> Task:
        return self._daily_tracker.add_task(title=title, details=details)

    def update_task(self, task: Task, status: TaskStatus) -> None:
        self._daily_tracker.update_task(task=task, status=status)


class AddTaskCommand(SessionHyperfocusCommand):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)
        self._task_command = TaskCommand(session)

    def execute(self, title: str, add_details: bool) -> None:
        details = printer.ask("Task details") if add_details else ""

        task = self._task_command.add_task(title=title, details=details)
        printer.success(
            text=formatter.task(task=task, show_prefix=True),
            event="created",
        )


class UpdateTaskCommand(SessionHyperfocusCommand):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)
        self._task_command = TaskCommand(session)

    def execute(self, task_id: int | None, status: TaskStatus, text: str) -> None:
        task_id = self._task_command.check_task_id_or_ask(
            task_id=task_id, text=text, exclude=[status]
        )

        task = self._task_command.get_task(task_id=task_id)
        if task.status == status.value:
            printer.warning(
                text=formatter.task(task=task, show_prefix=True),
                event="no change",
            )
            raise HyperfocusExit()

        self._task_command.update_task(task=task, status=status)
        printer.success(
            text=formatter.task(task=task, show_prefix=True),
            event="updated",
        )


class ShowTaskCommand(SessionHyperfocusCommand):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)
        self._task_command = TaskCommand(session)

    def execute(self, task_id: int | None) -> None:
        task_id = self._task_command.check_task_id_or_ask(
            task_id=task_id, text="Show task details"
        )

        task = self._task_command.get_task(task_id=task_id)
        printer.task(task=task, show_details=True, show_prefix=True)


class CopyCommand(SessionHyperfocusCommand):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)
        self._task_command = TaskCommand(session)

    def execute(self, task_id: int | None) -> None:
        task_id = self._task_command.check_task_id_or_ask(
            task_id=task_id, text="Copy task details"
        )

        task = self._task_command.get_task(task_id=task_id)
        if not task.details:
            raise TaskError(f"Task {task_id} does not have details.")

        pyperclip.copy(task.details)
        printer.success(f"Task {task_id} details copied to clipboard.", event="success")
