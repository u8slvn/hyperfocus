import pytest

from hyperfocus.commands.new_day import (
    CheckUnfinishedTasksCmd,
    NewDayCmd,
    ReviewUnfinishedTasksCmd,
)
from hyperfocus.database.models import Task
from hyperfocus.services import DailyTracker


@pytest.fixture
def printer(mocker):
    yield mocker.patch("hyperfocus.commands.new_day.printer")


def test_new_day_cmd_is_not_a_new_day(session, printer):
    session._daily_tracker.is_a_new_day.return_value = False

    NewDayCmd(session).execute()

    printer.new_day.assert_not_called()


def test_new_day_cmd_is_a_new_day(session, printer):
    session._daily_tracker.is_a_new_day.return_value = True

    NewDayCmd(session).execute()

    printer.new_day.assert_called_once()


class TestCheckUnfinishedTask:
    def test_check_unfinished_tasks_cmd(self, mocker, session, printer):
        previous_day = mocker.Mock(spec=DailyTracker, intance=True)
        previous_day.is_locked.return_value = False
        previous_day.get_tasks.return_value = [Task("foo")]
        session._daily_tracker.get_previous_day.return_value = previous_day

        CheckUnfinishedTasksCmd(session).execute()

        printer.banner.assert_called_once()

    def test_check_unfinished_tasks_cmd_with_no_previous_day(self, session, printer):
        session._daily_tracker.get_previous_day.return_value = None

        CheckUnfinishedTasksCmd(session).execute()

        printer.banner.assert_not_called()

    def test_check_unfinished_tasks_cmd_with_locked_previous_day(
        self, mocker, session, printer
    ):
        previous_day = mocker.Mock(spec=DailyTracker, intance=True)
        previous_day.is_locked.return_value = True
        session._daily_tracker.get_previous_day.return_value = previous_day

        CheckUnfinishedTasksCmd(session).execute()

        printer.banner.assert_not_called()

    def test_check_unfinished_tasks_cmd_with_no_tasks(self, mocker, session, printer):
        previous_day = mocker.Mock(spec=DailyTracker, intance=True)
        previous_day.is_locked.return_value = False
        previous_day.get_tasks.return_value = []
        session._daily_tracker.get_previous_day.return_value = previous_day

        CheckUnfinishedTasksCmd(session).execute()

        printer.banner.assert_not_called()


class TestReviewUnfinishedTasksCmd:
    @pytest.mark.parametrize(
        "confirmation, add_task_count",
        [
            ([True, True, True], 2),
            ([True, False, True], 1),
        ],
    )
    def test_review_unfinished_tasks(
        self, mocker, session, printer, confirmation, add_task_count
    ):
        previous_day = mocker.Mock(spec=DailyTracker, intance=True)
        previous_day.is_locked.return_value = False
        previous_day.get_tasks.return_value = [Task("foo"), Task("bar")]
        session._daily_tracker.get_previous_day.return_value = previous_day
        printer.confirm.side_effect = confirmation

        ReviewUnfinishedTasksCmd(session).execute()

        printer.echo.assert_called_once()
        assert session._daily_tracker.add_task.call_count == add_task_count
        previous_day.locked.assert_called_once()

    def test_review_unfinished_tasks_with_no_confirmation(
        self, mocker, session, printer
    ):
        previous_day = mocker.Mock(spec=DailyTracker, intance=True)
        previous_day.is_locked.return_value = False
        previous_day.get_tasks.return_value = [Task("foo")]
        session._daily_tracker.get_previous_day.return_value = previous_day
        printer.confirm.return_value = False

        ReviewUnfinishedTasksCmd(session).execute()

        printer.echo.assert_called_once()
        previous_day.locked.assert_called_once()

    def test_review_unfinished_tasks_cmd_with_no_previous_day(self, session, printer):
        session._daily_tracker.get_previous_day.return_value = None

        ReviewUnfinishedTasksCmd(session).execute()

        printer.echo.assert_not_called()

    def test_review_unfinished_tasks_cmd_with_locked_previous_day(
        self, mocker, session, printer
    ):
        previous_day = mocker.Mock(spec=DailyTracker, intance=True)
        previous_day.is_locked.return_value = True
        session._daily_tracker.get_previous_day.return_value = previous_day

        ReviewUnfinishedTasksCmd(session).execute()

        printer.echo.assert_not_called()

    def test_review_unfinished_tasks_cmd_with_not_tasks(self, mocker, session, printer):
        previous_day = mocker.Mock(spec=DailyTracker, intance=True)
        previous_day.is_locked.return_value = False
        previous_day.get_tasks.return_value = []
        session._daily_tracker.get_previous_day.return_value = previous_day

        ReviewUnfinishedTasksCmd(session).execute()

        printer.echo.assert_not_called()
