from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Generator

from hyperfocus.database.models import Task
from hyperfocus.database.models import WorkingDay
from hyperfocus.services.daily_tracker import DailyTracker


if TYPE_CHECKING:
    import datetime


class History:
    """
    Retrieve all tasks from the past days as history log.
    """

    def __init__(self, daily_tracker: DailyTracker) -> None:
        self.start = daily_tracker.date
        self.batch_size = 100

    def __call__(self) -> Generator[tuple[bool, datetime.date | Task], None, None]:
        """
        Return all date followed by tasks, all prefixed with a boolean which specify if
        the element is the last element of the list for the given date. This boolean
        is used later to manage pretty display.
        """
        offset = 0

        while True:
            query = WorkingDay.select()
            query = query.where(WorkingDay.date < self.start)
            query = query.order_by(WorkingDay.date.desc())
            query = query.limit(self.batch_size).offset(offset)
            previous_days_batch = list(query.execute())

            if not previous_days_batch:
                break

            for previous_day in previous_days_batch:
                daily_tracker = DailyTracker(previous_day)
                tasks = daily_tracker.get_tasks()

                if not tasks:
                    continue

                yield False, previous_day.date

                for i, task in enumerate(tasks):
                    last_element = i == len(tasks) - 1
                    yield last_element, task

            offset += self.batch_size
