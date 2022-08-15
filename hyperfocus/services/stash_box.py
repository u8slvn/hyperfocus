from __future__ import annotations

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.services.daily_tracker import DailyTracker
from hyperfocus.services.exceptions import StashBoxError


class StashBox:
    def __init__(self, daily_tracker: DailyTracker):
        self._daily_tracker = daily_tracker

    @staticmethod
    def get_tasks() -> list[Task]:
        query = Task.select().where(Task.status == TaskStatus.STASHED)
        tasks = list(query.execute())

        for i, task in enumerate(tasks):
            task.id = i + 1
            task.save()

        return tasks

    @property
    def tasks_count(self) -> int:
        return len(self.get_tasks())

    def add(self, task: Task) -> None:
        task.working_day = None
        task.id = self.tasks_count + 1
        task.status = TaskStatus.STASHED
        task.save()

    def pop(self, task_id: int) -> Task:
        tasks = self.get_tasks()
        try:
            task = tasks[task_id - 1]
        except IndexError:
            raise StashBoxError(f"Task {task_id} does not exist in stash box.")

        self._daily_tracker.add_task(task)

        return task

    def apply(self) -> None:
        for task in self.get_tasks():
            self._daily_tracker.add_task(task)

    @staticmethod
    def clear() -> None:
        Task.delete().where(Task.status == TaskStatus.STASHED).execute()
