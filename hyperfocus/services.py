from __future__ import annotations

import datetime
from typing import List

from hyperfocus.database.models import DailyTracker, Task, TaskStatus


class DailyTrackerService:
    def __init__(self, daily_tracker: DailyTracker, is_a_new_day: bool = False) -> None:
        self._base = daily_tracker
        self.is_a_new_day = is_a_new_day

    @classmethod
    def from_date(cls, date: datetime.date) -> DailyTrackerService:
        daily_tracker, is_a_new_day = DailyTracker.get_or_create(date=date)
        return cls(daily_tracker=daily_tracker, is_a_new_day=is_a_new_day)

    def get_previous_day(self) -> DailyTrackerService | None:
        query = DailyTracker.select()
        query = query.where(DailyTracker.date < self.date)
        query = query.order_by(DailyTracker.date.desc())
        previous_day = query.get_or_none()

        if not previous_day:
            return None

        return DailyTrackerService(previous_day)

    @property
    def date(self) -> datetime.date:
        return self._base.date

    def add_task(self, title: str, details: str | None = None) -> Task:
        details = details.strip() if isinstance(details, str) else details
        task = Task(
            id=self._base.next_task_id,
            title=title.strip(),
            details=details,
            status=TaskStatus.TODO,
            daily_tracker=self._base,
        )
        task.save()

        self._base.task_increment += 1
        self._base.save()

        return task

    def get_task(self, task_id: int) -> Task | None:
        return Task.get_or_none(Task.id == task_id, Task.daily_tracker == self._base)

    def get_tasks(self, exclude: list[TaskStatus] | None = None) -> List[Task]:
        exclude = exclude or []
        tasks = [task for task in self._base.tasks if task.status not in exclude]
        return tasks

    @staticmethod
    def update_task(task: Task, status: TaskStatus) -> None:
        task.status = status
        task.save()
