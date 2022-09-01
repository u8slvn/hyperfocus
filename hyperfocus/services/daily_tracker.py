from __future__ import annotations

import datetime
from typing import List

from hyperfocus.database.models import Task, TaskStatus, WorkingDay


class DailyTracker:
    """
    Each time the CLI is called, if it does not exist a working day is created in
    database with the current date. No working day matching with a date means that
    the CLI has not been used this specific day.
    The daily tracker wraps a working day and allows to perform every actions needed
    on it.
    """

    def __init__(self, working_day: WorkingDay, new_day: bool | None = None) -> None:
        self._working_day = working_day
        self._new_day = new_day
        self._previous_day: DailyTracker | None = None

    @property
    def date(self) -> datetime.date:
        return self._working_day.date

    def is_a_new_day(self):
        """
        Check if it is the first time that the CLI is called this day.
        """
        return self._new_day

    def is_locked(self):
        """
        Check if the daily tracker is locked.
        """
        return self._working_day.locked

    def locked(self):
        """
        Locked the daily tracker. It is used to prevent modification on past
        working day.
        """
        self._working_day.locked = True
        self._working_day.save()

    @classmethod
    def from_date(cls, date: datetime.date) -> DailyTracker:
        """
        Build the daily tracker from the given date.
        """
        working_day, new_day = WorkingDay.get_or_create(date=date)
        return cls(working_day=working_day, new_day=new_day)

    def get_previous_day(self) -> DailyTracker | None:
        """
        Fetch the daily tracker of the last working day. with activity.
        """
        if not self._previous_day:
            query = WorkingDay.select()
            query = query.where(WorkingDay.date < self.date)
            query = query.order_by(WorkingDay.date.desc())
            previous_day = query.get_or_none()

            if previous_day:
                self._previous_day = DailyTracker(previous_day)

        return self._previous_day

    def create_task(self, title: str, details: str | None = None) -> Task:
        """
        Create a new task associate to the working day.
        """
        details = details.strip() if isinstance(details, str) else details
        task = Task.create(
            id=self._working_day.next_task_id,
            title=title.strip(),
            details=details,
            status=TaskStatus.TODO,
            working_day=self._working_day,
        )
        self._working_day.save()

        return task

    def add_task(self, task: Task) -> Task:
        """
        Add an already created task to the working day.
        It's mainly used to add tasks from the stash box.
        """
        task.working_day = self._working_day
        task.id = self._working_day.next_task_id
        task.status = TaskStatus.TODO
        task.save()
        self._working_day.save()

        return task

    def copy_task(self, task: Task) -> Task:
        """
        Duplicate a task from another working day to the current one.
        """
        task = Task.create(
            id=self._working_day.next_task_id,
            title=task.title,
            details=task.details,
            status=TaskStatus.TODO,
            working_day=self._working_day,
            parent_task=task,
        )
        self._working_day.save()

        return task

    def get_task(self, task_id: int) -> Task | None:
        """
        Retrieve a task by id from the working day.
        """
        return Task.get_or_none(
            Task.id == task_id, Task.working_day == self._working_day
        )

    def get_tasks(self, exclude: list[TaskStatus] | None = None) -> List[Task]:
        """
        Get all tasks of the working day.
        """
        exclude = exclude or []

        query = self._working_day.tasks
        query = query.where(Task.status.not_in(exclude))
        query = query.order_by(Task.id.asc())

        return query.execute()

    @staticmethod
    def delete_task(task: Task) -> None:
        """
        Hard delete a task.
        """
        task.delete_instance()

    @staticmethod
    def update_task(task: Task, status: TaskStatus) -> None:
        """
        Persist an updated task.
        """
        task.status = status
        task.save()
