import datetime
from datetime import date

from hyperfocus.database.models import Task, TaskStatus, WorkingDay
from hyperfocus.services.daily_tracker import DailyTracker


def test_daily_tracker_new_day(test_database):
    daily_tracker1 = DailyTracker.from_date(datetime.date(2022, 2, 1))
    daily_tracker2 = DailyTracker.from_date(datetime.date(2022, 2, 1))

    assert daily_tracker1.is_a_new_day()
    assert not daily_tracker2.is_a_new_day()


def test_daily_tracker_locked(test_database):
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 2, 1))

    assert not daily_tracker.is_locked()

    daily_tracker.locked()

    assert daily_tracker.is_locked()


def test_daily_tracker_service_add_task(test_database):
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 1, 1))
    task = daily_tracker.create_task(title="Test add task", details="Test add details")

    working_day = WorkingDay.get(WorkingDay.date == daily_tracker.date)
    created_task = Task.get(
        Task.id == task.id,
        Task.working_day == working_day,
    )
    assert created_task.id == 1
    assert created_task.title == "Test add task"
    assert created_task.details == "Test add details"
    assert working_day.task_increment == 1


def test_daily_tracker_service_copy_task(test_database):
    daily_tracker1 = DailyTracker.from_date(datetime.date(2022, 1, 1))
    task1 = daily_tracker1.create_task(title="foo", details="bar")
    daily_tracker2 = DailyTracker.from_date(datetime.date(2022, 1, 2))
    task2 = daily_tracker2.copy_task(task1)

    copied_task = Task.get(
        Task.id == task2.id,
        Task.working_day == WorkingDay.get(WorkingDay.date == daily_tracker2.date),
    )
    assert copied_task.id == 1
    assert copied_task.title == task1.title
    assert copied_task.details == task1.details
    assert copied_task.parent_task == task1


def test_daily_tracker_service_get_task(test_database):
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 1, 2))
    _task = daily_tracker.create_task(title="Test add task", details="Test add details")

    task = daily_tracker.get_task(task_id=_task.id)

    assert task.id == _task.id
    assert task.title == _task.title
    assert task.details == _task.details


def test_daily_tracker_service_get_tasks(test_database):
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 1, 3))
    daily_tracker.create_task(title="Test add task 1", details="Test add details 1")
    daily_tracker.create_task(title="Test add task 2", details="Test add details 2")

    tasks = daily_tracker.get_tasks()

    assert len(tasks) == 2


def test_daily_tracker_service_get_tasks_with_exclude_status_filter(test_database):
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 1, 4))
    daily_tracker.create_task(title="Test add task 1", details="Test add details 1")
    daily_tracker.create_task(title="Test add task 2", details="Test add details 2")

    tasks = daily_tracker.get_tasks(exclude=[TaskStatus.TODO])

    assert len(tasks) == 0


def test_daily_tracker_service_update_task(test_database):
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 1, 5))
    _task = daily_tracker.create_task(title="Test add task", details="Test add details")

    daily_tracker.update_task(task=_task, status=TaskStatus.DONE)

    updated_task = daily_tracker.get_task(task_id=_task.id)
    assert updated_task.status == TaskStatus.DONE


def test_daily_tracker_service_get_date(test_database):
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 1, 6))

    assert daily_tracker.date == date(2022, 1, 6)


def test_daily_tracker_service_get_previous_day(test_database):
    _prev_day = DailyTracker.from_date(datetime.date(2022, 2, 1))
    _prev_day.create_task(title="Test1", details="1")
    _prev_day.create_task(title="Test2", details="2")
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 2, 2))

    previous_day = daily_tracker.get_previous_day()

    assert previous_day.date == date(2022, 2, 1)
    assert len(previous_day.get_tasks()) == 2


def test_daily_tracker_service_get_previous_day_return_none(test_database):
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 2, 1))

    previous_day = daily_tracker.get_previous_day()

    assert previous_day is None
