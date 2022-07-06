from datetime import date

from freezegun import freeze_time

from hyperfocus.models import DailyTracker, Task, TaskStatus
from hyperfocus.services import (
    DailyTrackerService,
    NullDailyTrackerService,
    PastTrackerService,
)


@freeze_time("2022-01-01")
def test_daily_tracker_service_add_task(test_db):
    daily_tracker = DailyTrackerService.today()

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


@freeze_time("2022-01-02")
def test_daily_tracker_service_get_task(test_db):
    daily_tracker = DailyTrackerService.today()
    _task = daily_tracker.add_task(title="Test add task", details="Test add details")

    task = daily_tracker.get_task(task_id=_task.id)

    assert task.id == _task.id
    assert task.title == _task.title
    assert task.details == _task.details


@freeze_time("2022-01-03")
def test_daily_tracker_service_get_tasks(test_db):
    daily_tracker = DailyTrackerService.today()
    daily_tracker.add_task(title="Test add task 1", details="Test add details 1")
    daily_tracker.add_task(title="Test add task 2", details="Test add details 2")

    tasks = daily_tracker.get_tasks()

    assert len(tasks) == 2


@freeze_time("2022-01-04")
def test_daily_tracker_service_get_tasks_with_exclude_status_filter(test_db):
    daily_tracker = DailyTrackerService.today()
    daily_tracker.add_task(title="Test add task 1", details="Test add details 1")
    daily_tracker.add_task(title="Test add task 2", details="Test add details 2")

    tasks = daily_tracker.get_tasks(exclude=[TaskStatus.TODO])

    assert len(tasks) == 0


@freeze_time("2022-01-05")
def test_daily_tracker_service_update_task(test_db):
    daily_tracker = DailyTrackerService.today()
    _task = daily_tracker.add_task(title="Test add task", details="Test add details")

    daily_tracker.update_task(task=_task, status=TaskStatus.DONE)

    updated_task = daily_tracker.get_task(task_id=_task.id)
    assert updated_task.status == TaskStatus.DONE


@freeze_time("2022-01-06")
def test_daily_tracker_service_get_date(test_db):
    daily_tracker_service = DailyTrackerService.today()

    assert daily_tracker_service.date == date(2022, 1, 6)


def test_past_tracker_get_past_tracker(test_db):
    with freeze_time("2022-01-10"):
        daily_tracker = DailyTrackerService.today()
        task1 = daily_tracker.add_task(title="test 1")
        task2 = daily_tracker.add_task(title="test 2")
        daily_tracker.update_task(task=task1, status=TaskStatus.DONE)
        daily_tracker.update_task(task=task2, status=TaskStatus.BLOCKED)
    with freeze_time("2022-01-11"):
        daily_tracker = DailyTrackerService.today()
        past_tracker = PastTrackerService(current_day=daily_tracker)

    previous_day = past_tracker.get_previous_day()

    assert isinstance(previous_day, DailyTrackerService)
    tasks = previous_day.get_tasks()
    assert previous_day.date == date(2022, 1, 10)
    assert len(tasks) == 2
    assert tasks[0].title == "test 1"
    assert tasks[1].title == "test 2"


def test_past_tracker_get_past_tracker_return_null_daily_tracker(test_db):
    with freeze_time("2022-01-18"):
        daily_tracker = DailyTrackerService.today()
        past_tracker = PastTrackerService(current_day=daily_tracker)

    previous_day = past_tracker.get_previous_day()

    assert isinstance(previous_day, NullDailyTrackerService)
    tasks = previous_day.get_tasks()
    assert tasks == []
    assert previous_day.date == date(1970, 1, 1)
