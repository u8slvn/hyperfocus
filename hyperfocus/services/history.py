from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hyperfocus.database.models import WorkingDay
from hyperfocus.services.daily_tracker import DailyTracker


if TYPE_CHECKING:
    import datetime

    from hyperfocus.database.models import Task


class History:
    def __init__(self, daily_tracker: DailyTracker) -> None:
        self.start = daily_tracker.date

    def __call__(self) -> Generator[datetime.date | Task, None, None]:
        query = WorkingDay.select()
        query = query.where(WorkingDay.date < self.start)
        query = query.order_by(WorkingDay.date.desc())
        previous_days = query.execute()

        for previous_day in previous_days:
            daily_tracker = DailyTracker(previous_day)
            yield previous_day.date

            for task in daily_tracker.get_tasks():
                yield task
