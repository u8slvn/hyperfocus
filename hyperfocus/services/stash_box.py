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

    def add(self, task: Task) -> None:
        task.working_day = None
        task.id = self.tasks_count + 1
        task.status = TaskStatus.STASHED
        task.save()

        self.tasks.append(task)

    def pop(self, task: Task, refresh_tasks: bool = True) -> None:
        task.working_day = self._daily_tracker.working_day
        task.status = TaskStatus.TODO
        task.save()

        if refresh_tasks:
            self.tasks.pop(task.id - 1)
            for i, task in enumerate(self.tasks):
                task.id = i + 1
                task.save()

    def apply(self) -> None:
        for task in self.tasks:
            self.pop(task, refresh_tasks=False)

        self._tasks = []

    def clear(self) -> None:
        for task in self.tasks:
            task.delete().execute()

        self._tasks = []
