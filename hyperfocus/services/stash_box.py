from __future__ import annotations

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.services.daily_tracker import DailyTracker


class StashBox:
    def __init__(self, daily_tracker: DailyTracker):
        self._daily_tracker = daily_tracker
        self._tasks: list[Task] | None = None

    @property
    def tasks(self) -> list[Task]:
        if self._tasks is None:
            query = Task.select().where(Task.status == TaskStatus.STASHED)
            self._tasks = list(query.execute())

        return self._tasks

    @property
    def tasks_count(self) -> int:
        return len(self.tasks)

    def add(self, task_id: int) -> Task | None:
        task = self._daily_tracker.get_task(task_id)

        if task is not None:
            task.working_day = None
            task.id = self.tasks_count + 1
            task.status = TaskStatus.STASHED
            task.save()

        self._tasks = None  # Reset tasks

        return task

    def pop(self, task_id: int) -> Task | None:
        task = self.tasks.pop(task_id - 1)

        if task is not None:
            task.working_day = self._daily_tracker.working_day
            task.status = TaskStatus.TODO
            task.save()

        for i, task in enumerate(self.tasks):
            task.id = i + 1
            task.save()

        return task
