from __future__ import annotations

from typing import TYPE_CHECKING

from hyperfocus import formatter
from hyperfocus.commands import SessionHyperfocusCommand, printer
from hyperfocus.database.models import TaskStatus
from hyperfocus.services import DailyTrackerService


if TYPE_CHECKING:
    from hyperfocus.session import Session


class NewDayCommand(SessionHyperfocusCommand):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    def execute(self):
        daily_tracker = DailyTrackerService.from_date(self._session.date)
        if not daily_tracker.is_a_new_day:
            return

        printer.echo(f"✨ {formatter.date(date=self._session.date)}")
        printer.echo("✨ A new day starts, good luck!\n")

        self._session.register_callback(self.review_unfinished_tasks)

    def review_unfinished_tasks(self) -> None:
        daily_tracker = DailyTrackerService.from_date(self._session.date)
        prev_day = daily_tracker.get_previous_day()
        if prev_day is None:
            return

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
                daily_tracker.add_task(title=task.title, details=task.details)
        printer.echo("")  # Empty line for design
