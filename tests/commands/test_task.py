import pytest

from hyperfocus.commands.task import CopyCommand, ShowTaskCommand, TaskCommand
from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.exceptions import HyperfocusExit, TaskError
from hyperfocus.services import DailyTrackerService


@pytest.fixture
def printer(mocker):
    yield mocker.patch("hyperfocus.commands.task.printer")


@pytest.fixture
def daily_tracker(mocker):
    daily_tracker = mocker.Mock(spec=DailyTrackerService, instance=True)
    mocker.patch(
        "hyperfocus.commands.task.DailyTrackerService.from_date",
        return_value=daily_tracker,
    )
    return daily_tracker


class TestTackCommand:
    def test_task_command_check_task_id_or_ask(
        self, mocker, test_session, printer, daily_tracker
    ):
        mocker.patch("hyperfocus.commands.task.TaskCommand.show_tasks")

        TaskCommand(test_session).check_task_id_or_ask(task_id=None, text="foobar")

        printer.ask.assert_called_once_with("foobar", type=int)

    def test_task_command_check_task_id_or_ask_do_not_ask(
        self, mocker, test_session, printer, daily_tracker
    ):
        mocker.patch("hyperfocus.commands.task.TaskCommand.show_tasks")

        TaskCommand(test_session).check_task_id_or_ask(task_id=1, text="foobar")

        printer.ask.assert_not_called()

    def test_task_command_show_tasks_with_no_tasks(
        self, mocker, test_session, printer, daily_tracker
    ):
        daily_tracker.get_tasks.return_value = []

        with pytest.raises(HyperfocusExit):
            TaskCommand(test_session).show_tasks(exclude=[TaskStatus.DONE])

        daily_tracker.get_tasks.assert_called_once_with(exclude=[TaskStatus.DONE])
        printer.echo.assert_called_once_with("No tasks for today...")
        printer.tasks.assert_not_called()

    def test_task_command_show_tasks(
        self, mocker, test_session, printer, daily_tracker
    ):
        daily_tracker.get_tasks.return_value = [mocker.sentinel.task]

        TaskCommand(test_session).show_tasks()

        daily_tracker.get_tasks.assert_called_once_with(exclude=[])
        printer.echo.assert_not_called()
        printer.tasks.assert_called_once_with(
            tasks=[mocker.sentinel.task], newline=False
        )

    def test_task_command_get_task(self, test_session, daily_tracker):
        daily_tracker.get_task.return_value = Task(id=1, title="foo", details="bar")

        task = TaskCommand(test_session).get_task(task_id=1)

        daily_tracker.get_task.assert_called_once_with(task_id=1)
        assert task.id == 1
        assert task.title == "foo"
        assert task.details == "bar"

    def test_task_command_get_task_fails(self, test_session, daily_tracker):
        daily_tracker.get_task.return_value = None

        with pytest.raises(TaskError, match=r"Task \d does not exist."):
            _ = TaskCommand(test_session).get_task(task_id=1)


@pytest.fixture
def pyperclip(mocker):
    yield mocker.patch("hyperfocus.commands.task.pyperclip")


@pytest.fixture
def task_command(mocker):
    task_command = mocker.Mock(spec=TaskCommand, instance=True)
    mocker.patch("hyperfocus.commands.task.TaskCommand", return_value=task_command)
    return task_command


class TestShowTaskCommand:
    def test_show_task_command(self, test_session, task_command, printer):
        task = Task(id=1, title="foo", details="bar")
        task_command.get_task.return_value = task
        ShowTaskCommand(test_session).execute(task_id=1)

        task_command.check_task_id_or_ask.assert_called_once_with(
            task_id=1, text="Show task details"
        )
        printer.task.assert_called_once_with(
            task=task, show_details=True, show_prefix=True
        )


class TestCopyCommand:
    def test_copy_command(self, test_session, printer, pyperclip, task_command):
        task1 = Task(id=1, title="foo", details="bar")
        task_command.check_task_id_or_ask.return_value = task1.id
        task_command.get_task.return_value = task1

        CopyCommand(test_session).execute(task_id=1)

        task_command.check_task_id_or_ask.assert_called_once_with(
            task_id=1, text="Copy task details"
        )
        pyperclip.copy.assert_called_once_with("bar")
        printer.success.assert_called_once_with(
            "Task 1 details copied to clipboard.", event="success"
        )

    def test_copy_command_fails(self, test_session, printer, pyperclip, task_command):
        task1 = Task(id=1, title="foo", details="")
        task_command.check_task_id_or_ask.return_value = task1.id
        task_command.get_task.return_value = task1

        with pytest.raises(TaskError, match=r"Task \d does not have details."):
            CopyCommand(test_session).execute(task_id=1)

        task_command.check_task_id_or_ask.assert_called_once_with(
            task_id=1, text="Copy task details"
        )
        pyperclip.copy.assert_not_called()
        printer.success.assert_not_called()
