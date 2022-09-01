from __future__ import annotations

from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.services.daily_tracker import DailyTracker
from hyperfocus.services.exceptions import StashBoxError


class StashBox:
    """
    Provide an option to store a task and retrieve it later.
    """

    def __init__(self, daily_tracker: DailyTracker):
        self._daily_tracker = daily_tracker

    @staticmethod
    def get_tasks() -> list[Task]:
        """
        List all the tasks from the stash box.
        """
        query = Task.select().where(Task.status == TaskStatus.STASHED)
        tasks = list(query.execute())

        for i, task in enumerate(tasks):
            task.id = i + 1
            task.save()

        return tasks

    @property
    def tasks_count(self) -> int:
        """
        Return the number of tasks in the stash box.
        """
        return len(self.get_tasks())

    def add(self, task: Task) -> None:
        """
        Push a task into the stash box.
        """
        task.working_day = None
        task.id = self.tasks_count + 1
        task.status = TaskStatus.STASHED
        task.save()

    def pop(self, task_id: int) -> Task:
        """
        Retrieve a task from the stash box and add it to the current working day.
        """
        tasks = self.get_tasks()
        try:
            task = tasks[task_id - 1]
        except IndexError:
            raise StashBoxError(f"Task {task_id} does not exist in stash box.")

        self._daily_tracker.add_task(task)

        return task

    def apply(self) -> None:
        """
        Apply every task from the stash box to the current working day.
        """
        for task in self.get_tasks():
            self._daily_tracker.add_task(task)

    @staticmethod
    def clear() -> None:
        """
        Delete all the tasks in the stash box.
        """
        Task.delete().where(Task.status == TaskStatus.STASHED).execute()
