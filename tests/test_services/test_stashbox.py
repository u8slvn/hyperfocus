import datetime

from hyperfocus.database.models import TaskStatus
from hyperfocus.services.daily_tracker import DailyTracker
from hyperfocus.services.stash_box import StashBox


def test_add(test_database):
    date = datetime.date(2022, 1, 1)
    daily_tracker = DailyTracker.from_date(date=date)
    task = daily_tracker.create_task("foo")
    stash_box = StashBox(daily_tracker)

    stash_box.add(task)

    assert len(daily_tracker.get_tasks()) == 0
    assert task.working_day is None
    assert task.id == 1
    assert task.status == TaskStatus.STASHED


def test_pop(test_database):
    date = datetime.date(2022, 1, 1)
    daily_tracker = DailyTracker.from_date(date=date)
    stash_box = StashBox(daily_tracker)
    task1 = daily_tracker.create_task("foo")
    stash_box.add(task1)
    task2 = daily_tracker.create_task("bar")
    stash_box.add(task2)

    assert len(daily_tracker.get_tasks()) == 0
    assert stash_box.tasks_count == 2
    assert task2.id == 2

    stash_box.pop(task1)

    assert len(daily_tracker.get_tasks()) == 1
    assert stash_box.tasks_count == 1
    assert stash_box.tasks[0].uuid == task2.uuid
    assert stash_box.tasks[0].id == 1


def test_apply(test_database):
    date = datetime.date(2022, 1, 1)
    daily_tracker = DailyTracker.from_date(date=date)
    stash_box = StashBox(daily_tracker)
    task1 = daily_tracker.create_task("foo")
    stash_box.add(task1)
    task2 = daily_tracker.create_task("bar")
    stash_box.add(task2)

    assert len(daily_tracker.get_tasks()) == 0
    assert stash_box.tasks_count == 2

    stash_box.apply()

    assert len(daily_tracker.get_tasks()) == 2
    assert stash_box.tasks_count == 0


def test_clear(test_database):
    date = datetime.date(2022, 1, 1)
    daily_tracker = DailyTracker.from_date(date=date)
    stash_box = StashBox(daily_tracker)
    task1 = daily_tracker.create_task("foo")
    stash_box.add(task1)
    task2 = daily_tracker.create_task("bar")
    stash_box.add(task2)

    assert len(daily_tracker.get_tasks()) == 0
    assert stash_box.tasks_count == 2

    stash_box.clear()

    assert len(daily_tracker.get_tasks()) == 0
    assert stash_box.tasks_count == 0
