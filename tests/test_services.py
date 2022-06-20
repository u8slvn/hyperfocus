from datetime import datetime

from freezegun import freeze_time

from hyperfocus.models import DailyTracker, Task, TaskStatus
from hyperfocus.services import DailyTrackerService


@freeze_time("2022-01-01")
def test_daily_tracker_service_add_task():
    date = datetime.now().date()
    daily_tracker_service = DailyTrackerService(date=date)

    task = daily_tracker_service.add_task(
        title="Test add task", details="Test add details"
    )

    created_daily_tracker = DailyTracker.get(DailyTracker.date == date)
    created_task = Task.get(
        Task.id == task.id,
        Task.daily_tracker == created_daily_tracker,
    )
    assert created_task.id == 1
    assert created_task.title == "Test add task"
    assert created_task.details == "Test add details"
    assert created_daily_tracker.task_increment == 1


@freeze_time("2022-01-02")
def test_daily_tracker_service_get_task():
    date = datetime.now().date()
    daily_tracker_service = DailyTrackerService(date=date)
    _task = daily_tracker_service.add_task(
        title="Test add task", details="Test add details"
    )

    task = daily_tracker_service.get_task(id=_task.id)

    assert task.id == _task.id
    assert task.title == _task.title
    assert task.details == _task.details


@freeze_time("2022-01-03")
def test_daily_tracker_service_get_tasks():
    date = datetime.now().date()
    daily_tracker_service = DailyTrackerService(date=date)
    daily_tracker_service.add_task(
        title="Test add task 1", details="Test add details 1"
    )
    daily_tracker_service.add_task(
        title="Test add task 2", details="Test add details 2"
    )

    tasks = daily_tracker_service.get_tasks()

    assert len(tasks) == 2


@freeze_time("2022-01-04")
def test_daily_tracker_service_get_tasks_with_exclude_status_filter():
    date = datetime.now().date()
    daily_tracker_service = DailyTrackerService(date=date)
    daily_tracker_service.add_task(
        title="Test add task 1", details="Test add details 1"
    )
    daily_tracker_service.add_task(
        title="Test add task 2", details="Test add details 2"
    )

    tasks = daily_tracker_service.get_tasks(exclude=[TaskStatus.TODO])

    assert len(tasks) == 0


@freeze_time("2022-01-05")
def test_daily_tracker_service_update_task():
    date = datetime.now().date()
    daily_tracker_service = DailyTrackerService(date=date)
    _task = daily_tracker_service.add_task(
        title="Test add task", details="Test add details"
    )

    daily_tracker_service.update_task(task=_task, status=TaskStatus.DONE)

    updated_task = daily_tracker_service.get_task(id=_task.id)
    assert updated_task.status == TaskStatus.DONE


@freeze_time("2022-01-06")
def test_daily_tracker_service_get_date():
    date = datetime.now().date()
    daily_tracker_service = DailyTrackerService(date=date)

    assert daily_tracker_service.date == datetime(2022, 1, 6).date()
