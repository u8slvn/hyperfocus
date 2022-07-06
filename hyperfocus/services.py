import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

from hyperfocus.models import DailyTracker, Task, TaskStatus


class DailyTrackerServiceBase(ABC):
    @property
    @abstractmethod
    def date(self) -> datetime.date:
        raise NotImplementedError

    @abstractmethod
    def add_task(self, title: str, details: Optional[str] = None) -> Task:
        raise NotImplementedError

    @abstractmethod
    def get_task(self, task_id: int) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_tasks(self, exclude: Optional[List[TaskStatus]] = None) -> List[Task]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update_task(task: Task, status: TaskStatus) -> None:
        raise NotImplementedError


class DailyTrackerService(DailyTrackerServiceBase):
    def __init__(self, daily_tracker: DailyTracker, new_day: bool = False):
        self._base = daily_tracker
        self.new_day = new_day

    @classmethod
    def today(cls) -> "DailyTrackerService":
        now = datetime.datetime.now().date()
        daily_tracker, new_day = DailyTracker.get_or_create(date=now)

        return cls(daily_tracker=daily_tracker, new_day=new_day)

    @property
    def date(self) -> datetime.date:
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

    def get_tasks(self, exclude: Optional[List[TaskStatus]] = None) -> List[Task]:
        exclude = exclude or []
        tasks = [task for task in self._base.tasks if task.status not in exclude]
        return tasks

    @staticmethod
    def update_task(task: Task, status: TaskStatus) -> None:
        task.status = status
        task.save()


class NullDailyTrackerService(DailyTrackerServiceBase):
    null_date = datetime.datetime(1970, 1, 1).date()

    def __init__(self, date: Optional[datetime.date] = None):
        self._date = date or self.null_date
        self.daily_tracker = None
        self.new_day = None

    @property
    def date(self) -> datetime.date:
        return self._date

    def add_task(self, title: str, details: Optional[str] = None) -> Task:
        pass

    def get_task(self, task_id: int) -> Optional[Task]:
        pass

    def get_tasks(self, exclude: Optional[List[TaskStatus]] = None) -> List[Task]:
        return []

    @staticmethod
    def update_task(task: Task, status: TaskStatus) -> None:
        pass


class PastTrackerService:
    def __init__(self, current_day: DailyTrackerService):
        self._current_day = current_day

    def get_previous_day(self) -> Optional["DailyTrackerServiceBase"]:
        date = self._current_day.date
        previous_daily_tracker = (
            DailyTracker.select()
            .where(DailyTracker.date < date)
            .order_by(DailyTracker.date.desc())
            .get_or_none()
        )
        if not previous_daily_tracker:
            return NullDailyTrackerService()

        return DailyTrackerService(daily_tracker=previous_daily_tracker)
