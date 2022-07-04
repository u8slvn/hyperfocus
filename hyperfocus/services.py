from typing import List, Optional

from hyperfocus.models import DailyTracker, Task, TaskStatus


class DailyTrackerService:
    def __init__(self, date):
        self._base, self.new_day = DailyTracker.get_or_create(date=date)

    @property
    def date(self) -> str:
        return self._base.date

    def add_task(self, title: str, details: Optional[str] = None) -> Task:
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

    def get_task(self, task_id: int) -> Optional[Task]:
        return Task.get_or_none(Task.id == task_id, Task.daily_tracker == self._base)

    def get_tasks(self, exclude: Optional[List[TaskStatus]] = None) -> List:
        exclude = exclude or []
        tasks = [task for task in self._base.tasks if task.status not in exclude]
        return tasks

    @staticmethod
    def update_task(task: Task, status: TaskStatus) -> None:
        task.status = status
        task.save()
