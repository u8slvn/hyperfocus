import datetime

from hyperfocus.database.models import Task
from hyperfocus.services.daily_tracker import DailyTracker
from hyperfocus.services.history import History


def test_history(test_database):
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 2, 1))
    daily_tracker.create_task("task1")
    daily_tracker.create_task("task2")
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 2, 2))
    daily_tracker.create_task("task3")
    daily_tracker.create_task("task4")
    daily_tracker = DailyTracker.from_date(datetime.date(2022, 2, 3))
    history = History(daily_tracker)

    result = [data for data in history()]

    assert len(result) == 6
    assert isinstance(result[0], datetime.date)
    assert isinstance(result[1], Task)
    assert isinstance(result[2], Task)
    assert isinstance(result[3], datetime.date)
    assert isinstance(result[4], Task)
    assert isinstance(result[5], Task)
