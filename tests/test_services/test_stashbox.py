import datetime

from hyperfocus.database.models import TaskStatus
from hyperfocus.services.daily_tracker import DailyTracker
from hyperfocus.services.stash_box import StashBox


def test_add(test_database):
    date = datetime.date(2022, 1, 1)
    daily_tracker = DailyTracker.from_date(date=date)
    task = daily_tracker.create_task("foo")
    stash_box = StashBox(daily_tracker)

    task = stash_box.add(task.id)

    assert len(daily_tracker.get_tasks()) == 0
    assert task.working_day is None
    assert task.id == 1
    assert task.status == TaskStatus.STASHED


def test_pop(test_database):
    date = datetime.date(2022, 1, 1)
    daily_tracker = DailyTracker.from_date(date=date)
    stash_box = StashBox(daily_tracker)
    task1 = daily_tracker.create_task("foo")
    stash_box.add(task1.id)
    task2 = daily_tracker.create_task("bar")
    stash_box.add(task2.id)

    assert len(daily_tracker.get_tasks()) == 0
    assert stash_box.tasks_count == 2
    assert task2.id == 2

    stash_box.pop(1)

    assert len(daily_tracker.get_tasks()) == 1
    assert stash_box.tasks_count == 1
    assert stash_box.tasks[0].uuid == task2.uuid
    assert stash_box.tasks[0].id == 1
