from __future__ import annotations

import re

from typing import TYPE_CHECKING
from typing import cast

import click

from hyperfocus.console.core import parameters
from hyperfocus.console.exceptions import HyperfocusExit
from hyperfocus.console.exceptions import TaskError
from hyperfocus.database.models import TaskStatus
from hyperfocus.termui import formatter
from hyperfocus.termui import printer
from hyperfocus.termui import prompt
from hyperfocus.termui import style
from hyperfocus.termui.components import SuccessNotification
from hyperfocus.termui.components import TasksTable
from hyperfocus.termui.components import WarningNotification


if TYPE_CHECKING:
    from hyperfocus.database.models import Task
    from hyperfocus.services.daily_tracker import DailyTracker
    from hyperfocus.services.session import Session


class TaskCommands:
    comment_line_re = r"^#.*\n?"

    def __init__(self, session: Session) -> None:
        self.session = session

    def show_tasks(self) -> None:
        tasks = self.session.daily_tracker.get_tasks()

        if not tasks:
            printer.echo("No tasks for today...")
            raise HyperfocusExit()

        printer.echo(TasksTable(tasks))

    def pick_task(self, prompt_text: str) -> int:
        self.show_tasks()
        return cast(int, prompt.prompt(prompt_text, type=click.INT))

    def pick_tasks(self, prompt_text: str) -> tuple[int]:
        self.show_tasks()
        return tuple(prompt.prompt(prompt_text, type=parameters.INT_LIST))

    def get_task(self, task_id: int) -> Task:
        task = self.session.daily_tracker.get_task(task_id)
        if not task:
            raise TaskError(f"Task {task_id} does not exist.")

        return task

    def get_tasks(self, task_ids: tuple[int, ...], prompt_text: str) -> list[Task]:
        if not task_ids:
            task_ids = self.pick_tasks(prompt_text=prompt_text)

        tasks = []
        for task_id in task_ids:
            task = self.get_task(task_id)
            tasks.append(task)

        return tasks

    def update_tasks_status(self, tasks: list[Task], status: TaskStatus) -> None:
        for task in tasks:
            if task.status == status.value:
                printer.echo(
                    WarningNotification(
                        f"{formatter.task(task=task, show_prefix=True)} "
                        f"[{style.INFO}]unchanged[/]."
                    )
                )
                continue

            task.status = status
            self.session.daily_tracker.update_task(task=task)

            text_suffix = "reset" if status == TaskStatus.TODO else status.name.lower()
            printer.echo(
                SuccessNotification(
                    f"{formatter.task(task=task, show_prefix=True)} "
                    f"[{style.INFO}]{text_suffix}[/]."
                )
            )

    def edit_task(self, task: Task, field: str, splitlines: bool = False) -> bool:
        """Edit task field.

        Return a boolean indicating if the field has been edited.
        """
        assert hasattr(task, field), f"Task does not have field {field}"

        comment = f"\n# Edit {field} of Task #{task.id}. Lines starting with '#' will be ignored.\n"
        old_value = getattr(task, field)
        new_value = click.edit(f"{old_value}{comment}")

        if new_value is None:  # Do nothing if the field is unchanged
            return False

        new_value = re.sub(self.comment_line_re, "", new_value, flags=re.MULTILINE)
        new_value = "".join(new_value.splitlines()) if splitlines else new_value
        new_value = new_value.strip()

        setattr(task, field, new_value)
        return True


class TasksReviewer:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _get_unfinished_task(previous_day: DailyTracker) -> list[Task]:
        unfinished_tasks = []
        if previous_day and not previous_day.is_locked():
            finished_status = [TaskStatus.DELETED, TaskStatus.DONE]
            unfinished_tasks = previous_day.get_tasks(exclude=finished_status)

        return unfinished_tasks

    def show_review_reminder(self) -> None:
        previous_day = self.session.daily_tracker.get_previous_day()
        if previous_day is None:
            return

        unfinished_tasks = self._get_unfinished_task(previous_day)
        if len(unfinished_tasks) > 0 and previous_day:
            printer.banner(
                f"You have {len(unfinished_tasks)} unfinished task(s) from "
                f"{formatter.date(date=previous_day.date)}, run 'hyf' "
                f"to review."
            )

    def review_tasks(self) -> None:
        previous_day = self.session.daily_tracker.get_previous_day()
        if previous_day is None:
            return

        unfinished_tasks = self._get_unfinished_task(previous_day)

        if (
            len(unfinished_tasks) > 0
            and previous_day
            and prompt.confirm(
                f"Review [{style.INFO}]{len(unfinished_tasks)}[/] unfinished task(s) "
                f"from {formatter.date(date=previous_day.date)}",
                default=True,
            )
        ):
            for task in unfinished_tasks:
                if prompt.confirm(f'Continue "[{style.INFO}]{task.title}[/]"'):
                    self.session.daily_tracker.copy_task(task)

        if previous_day:
            previous_day.locked()
