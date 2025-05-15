from __future__ import annotations

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
    history.batch_size = 2  # Set a smaller batch size for testing

    result = [data for data in history()]

    assert len(result) == 6
    assert result[0][0] is False
    assert isinstance(result[0][1], datetime.date)
    assert result[1][0] is False
    assert isinstance(result[1][1], Task)
    assert result[2][0] is True
    assert isinstance(result[2][1], Task)
    assert result[3][0] is False
    assert isinstance(result[3][1], datetime.date)
    assert result[4][0] is False
    assert isinstance(result[4][1], Task)
    assert result[5][0] is True
    assert isinstance(result[5][1], Task)
