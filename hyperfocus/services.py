from datetime import datetime
from typing import List, Optional

from hyperfocus.config import Config
from hyperfocus.database import database
from hyperfocus.models import DailyTracker, Status, Task


class Session:
    def __init__(self):
        config = Config.load()
        database.connect(db_path=config.db_path)
        now = datetime.now().date()
        self.daily_tracker_service: DailyTrackerService = DailyTrackerService(date=now)

    def is_a_new_day(self) -> bool:
        return self.daily_tracker_service.new_day

    @property
    def date(self):
        return self.daily_tracker_service.date


class DailyTrackerService:
    def __init__(self, date: datetime.date):
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
            status=Status.TODO.value,
            daily_tracker=self._base,
        )
        task.save()

        self._base.task_increment += 1
        self._base.save()

        return task

    def get_task(self, id: int) -> Optional[Task]:
        return Task.get_or_none(Task.id == id, Task.daily_tracker == self._base)

    def get_tasks(self, exclude: Optional[List[Status]] = None) -> List:
        exclude = exclude or []
        tasks = [
            task for task in self._base.tasks if Status(task.status) not in exclude
        ]
        return tasks

    def update_task(self, task: Task, status: Status) -> None:
        task.status = status.value
        task.save()
