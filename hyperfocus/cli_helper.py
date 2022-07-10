from __future__ import annotations

from typing import TYPE_CHECKING

from hyperfocus import formatter
from hyperfocus.commands import printer
from hyperfocus.database.models import TaskStatus


if TYPE_CHECKING:
    from hyperfocus.session import Session


class CLIHelper:
    def __init__(self, session: Session):
        self._session = session


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
