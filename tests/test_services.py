import datetime
from datetime import date

from hyperfocus.database.models import DailyTracker, Task, TaskStatus
from hyperfocus.services import (
    DailyTrackerService,
    NullDailyTrackerService,
    PastTrackerService,
)


def test_daily_tracker_service_add_task(test_database):
    daily_tracker = DailyTrackerService.from_date(datetime.date(2022, 1, 1))

    task = daily_tracker.add_task(title="Test add task", details="Test add details")

    created_daily_tracker = DailyTracker.get(DailyTracker.date == daily_tracker.date)
    created_task = Task.get(
        Task.id == task.id,
        Task.daily_tracker == created_daily_tracker,
    )
    assert created_task.id == 1
    assert created_task.title == "Test add task"
    assert created_task.details == "Test add details"
    assert created_daily_tracker.task_increment == 1


def test_daily_tracker_service_get_task(test_database):
    daily_tracker = DailyTrackerService.from_date(datetime.date(2022, 1, 2))
    _task = daily_tracker.add_task(title="Test add task", details="Test add details")

    task = daily_tracker.get_task(task_id=_task.id)

    assert task.id == _task.id
    assert task.title == _task.title
    assert task.details == _task.details


def test_daily_tracker_service_get_tasks(test_database):
    daily_tracker = DailyTrackerService.from_date(datetime.date(2022, 1, 3))
    daily_tracker.add_task(title="Test add task 1", details="Test add details 1")
    daily_tracker.add_task(title="Test add task 2", details="Test add details 2")

    tasks = daily_tracker.get_tasks()

    assert len(tasks) == 2


def test_daily_tracker_service_get_tasks_with_exclude_status_filter(test_database):
    daily_tracker = DailyTrackerService.from_date(datetime.date(2022, 1, 4))
    daily_tracker.add_task(title="Test add task 1", details="Test add details 1")
    daily_tracker.add_task(title="Test add task 2", details="Test add details 2")

    tasks = daily_tracker.get_tasks(exclude=[TaskStatus.TODO])

    assert len(tasks) == 0


def test_daily_tracker_service_update_task(test_database):
    daily_tracker = DailyTrackerService.from_date(datetime.date(2022, 1, 5))
    _task = daily_tracker.add_task(title="Test add task", details="Test add details")

    daily_tracker.update_task(task=_task, status=TaskStatus.DONE)

    updated_task = daily_tracker.get_task(task_id=_task.id)
    assert updated_task.status == TaskStatus.DONE


def test_daily_tracker_service_get_date(test_database):
    daily_tracker = DailyTrackerService.from_date(datetime.date(2022, 1, 6))

    assert daily_tracker.date == date(2022, 1, 6)


def test_past_tracker_get_past_tracker(test_database):
    daily_tracker = DailyTrackerService.from_date(datetime.date(2022, 1, 10))
    task1 = daily_tracker.add_task(title="test 1")
    task2 = daily_tracker.add_task(title="test 2")
    daily_tracker.update_task(task=task1, status=TaskStatus.DONE)
    daily_tracker.update_task(task=task2, status=TaskStatus.BLOCKED)
    daily_tracker = DailyTrackerService.from_date(datetime.date(2022, 1, 11))
    past_tracker = PastTrackerService(current_day=daily_tracker)

    previous_day = past_tracker.get_previous_day()

    assert isinstance(previous_day, DailyTrackerService)
    tasks = previous_day.get_tasks()
    assert previous_day.date == date(2022, 1, 10)
    assert len(tasks) == 2
    assert tasks[0].title == "test 1"
    assert tasks[1].title == "test 2"


def test_past_tracker_get_past_tracker_return_null_daily_tracker(test_database):
    daily_tracker = DailyTrackerService.from_date(datetime.date(2022, 1, 18))
    past_tracker = PastTrackerService(current_day=daily_tracker)

    previous_day = past_tracker.get_previous_day()

    assert isinstance(previous_day, NullDailyTrackerService)
    tasks = previous_day.get_tasks()
    assert tasks == []
    assert previous_day.date == date(1970, 1, 1)
