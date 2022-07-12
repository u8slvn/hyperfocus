from __future__ import annotations

import datetime
from typing import List

from hyperfocus.database.models import Task, TaskStatus, WorkingDay


class DailyTracker:
    def __init__(self, working_day: WorkingDay, is_a_new_day: bool = False) -> None:
        self._working_day = working_day
        self.is_a_new_day = is_a_new_day

    @classmethod
    def from_date(cls, date: datetime.date) -> DailyTracker:
        working_day, is_a_new_day = WorkingDay.get_or_create(date=date)
        return cls(working_day=working_day, is_a_new_day=is_a_new_day)

    def get_previous_day(self) -> DailyTracker | None:
        query = WorkingDay.select()
        query = query.where(WorkingDay.date < self.date)
        query = query.order_by(WorkingDay.date.desc())
        previous_day = query.get_or_none()

        if not previous_day:
            return None

        return DailyTracker(previous_day)

    @property
    def date(self) -> datetime.date:
        return self._working_day.date

    def add_task(self, title: str, details: str | None = None) -> Task:
        details = details.strip() if isinstance(details, str) else details
        task = Task.create(
            id=self._working_day.next_task_id,
            title=title.strip(),
            details=details,
            status=TaskStatus.TODO,
            daily_tracker=self._working_day,
        )
        self._working_day.save()

        return task

    def get_task(self, task_id: int) -> Task | None:
        return Task.get_or_none(
            Task.id == task_id, Task.daily_tracker == self._working_day
        )

    def get_tasks(self, exclude: list[TaskStatus] | None = None) -> List[Task]:
        exclude = exclude or []
        tasks = [task for task in self._working_day.tasks if task.status not in exclude]
        return tasks

    @staticmethod
    def update_task(task: Task, status: TaskStatus) -> None:
        task.status = status
        task.save()
