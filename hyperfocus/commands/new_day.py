from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, cast

from hyperfocus.commands import SessionHyperfocusCommand
from hyperfocus.database.models import TaskStatus
from hyperfocus.services import DailyTracker
from hyperfocus.termui import formatter, printer


if TYPE_CHECKING:
    from hyperfocus.database.models import Task
    from hyperfocus.session import Session


class NewDayCmd(SessionHyperfocusCommand):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    def execute(self):
        if not self._session.daily_tracker.is_a_new_day():
            return

        printer.new_day(f"{formatter.date(date=self._session.date)}")
        printer.new_day("A new day starts, good luck!\n")


class UnfinishedTasksCmd(SessionHyperfocusCommand, ABC):
    def __init__(self, session: Session):
        super().__init__(session=session)
        self._previous_day = self._session.daily_tracker.get_previous_day()

    def get_unfinished_tasks(self) -> list[Task]:
        if self._previous_day is None or self._previous_day.is_locked():
            return []

        finished_status = [TaskStatus.DELETED, TaskStatus.DONE]
        return self._previous_day.get_tasks(exclude=finished_status)


class CheckUnfinishedTasksCmd(UnfinishedTasksCmd):
    def execute(self) -> None:
        unfinished_tasks_count = len(self.get_unfinished_tasks())

        if unfinished_tasks_count < 1:
            return

        self._previous_day = cast(DailyTracker, self._previous_day)
        printer.banner(
            f"You have {unfinished_tasks_count} unfinished task(s) from "
            f"{formatter.date(date=self._previous_day.date)}, run 'hyf' "
            f"to review."
        )


class ReviewUnfinishedTasksCmd(UnfinishedTasksCmd):
    def execute(self) -> None:
        unfinished_tasks = self.get_unfinished_tasks()
        if not unfinished_tasks:
            return

        self._previous_day = cast(DailyTracker, self._previous_day)
        printer.echo(
            f"Unfinished task(s) from {formatter.date(date=self._previous_day.date)}:"
        )
        printer.tasks(tasks=unfinished_tasks)
        if not printer.confirm(
            f"Review {len(unfinished_tasks)} unfinished task(s)",
            default=True,
        ):
            return

        for task in unfinished_tasks:
            if printer.confirm(f'Take back task "{task.title}" for today'):
                self._session.daily_tracker.add_task(
                    title=task.title, details=task.details
                )

        self._previous_day.locked()
