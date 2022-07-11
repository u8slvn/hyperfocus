import pytest

from hyperfocus.commands.cmd_new_day import NewDayCommand
from hyperfocus.database.models import Task
from hyperfocus.services import DailyTrackerService


@pytest.fixture
def printer(mocker):
    yield mocker.patch("hyperfocus.commands.cmd_new_day.printer")


@pytest.fixture
def daily_tracker(mocker):
    daily_tracker = mocker.Mock(spec=DailyTrackerService, intsance=True)
    mocker.patch(
        "hyperfocus.commands.cmd_new_day.DailyTrackerService",
        **{"from_date.return_value": daily_tracker}
    )
    yield daily_tracker


def test_new_day_command_is_not_a_new_day(test_session, daily_tracker, printer):
    daily_tracker.is_a_new_day = False

    NewDayCommand(test_session).execute()

    printer.echo.assert_not_called()
    assert test_session.callback_commands == []


def test_new_day_command_is_a_new_day(test_session, daily_tracker, printer):
    daily_tracker.is_a_new_day = True

    new_day_cmd = NewDayCommand(test_session)
    new_day_cmd.execute()

    assert printer.echo.call_count == 2
    assert test_session.callback_commands == [new_day_cmd.review_unfinished_tasks]


def test_review_unfinished_tasks_with_no_previous_day(
    test_session, daily_tracker, printer
):
    daily_tracker.get_previous_day.return_value = None

    new_day_cmd = NewDayCommand(test_session)
    new_day_cmd.review_unfinished_tasks()

    printer.confirm.assert_not_called()
    printer.echo.assert_not_called()


def test_review_unfinished_tasks_with_no_task(
    mocker, test_session, daily_tracker, printer
):
    prev_day = mocker.Mock(spec=DailyTrackerService, instance=True)
    daily_tracker.get_previous_day.return_value = prev_day
    prev_day.get_tasks.return_value = []

    new_day_cmd = NewDayCommand(test_session)
    new_day_cmd.review_unfinished_tasks()

    printer.confirm.assert_not_called()
    printer.echo.assert_not_called()


def test_review_unfinished_tasks_with_task_respond_no(
    mocker, test_session, daily_tracker, printer
):
    prev_day = mocker.Mock(spec=DailyTrackerService, instance=True)
    daily_tracker.get_previous_day.return_value = prev_day
    prev_day.get_tasks.return_value = [Task(id=1, title="foobar")]
    printer.confirm.return_value = False

    new_day_cmd = NewDayCommand(test_session)
    new_day_cmd.review_unfinished_tasks()

    assert printer.echo.call_count == 1
    assert printer.confirm.call_count == 1


def test_review_unfinished_tasks_with_task_respond_yes(
    mocker, test_session, daily_tracker, printer
):
    prev_day = mocker.Mock(spec=DailyTrackerService, instance=True)
    daily_tracker.get_previous_day.return_value = prev_day
    prev_day.get_tasks.return_value = [Task(id=1, title="foobar")]
    printer.confirm.return_value = True

    new_day_cmd = NewDayCommand(test_session)
    new_day_cmd.review_unfinished_tasks()

    assert printer.echo.call_count == 2
    assert printer.confirm.call_count == 2
    daily_tracker.add_task.assert_called_once_with(title="foobar", details=None)
