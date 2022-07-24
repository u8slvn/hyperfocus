import pytest

from hyperfocus.console.commands.task import (
    AddTaskCmd,
    CopyTaskDetailsCmd,
    ListTaskCmd,
    ShowTaskCmd,
    TaskCmd,
    UpdateTasksCmd,
)
from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.exceptions import HyperfocusExit, TaskError


@pytest.fixture
def printer(mocker):
    yield mocker.patch("hyperfocus.console.commands.task.printer")


@pytest.fixture
def prompt(mocker):
    yield mocker.patch("hyperfocus.console.commands.task.prompt")


@pytest.fixture
def pyperclip(mocker):
    yield mocker.patch("hyperfocus.console.commands.task.pyperclip")


@pytest.fixture
def formatter(mocker):
    yield mocker.patch("hyperfocus.console.commands.task.formatter")


class TestTaskCmd:
    def test_get_task(self, mocker, session, printer):
        session._daily_tracker.get_task.return_value = mocker.sentinel.task

        task = TaskCmd(session).get_task(1)

        assert task == mocker.sentinel.task
        session._daily_tracker.get_task.assert_called_once_with(task_id=1)

    def test_get_task_fails(self, session, printer):
        session._daily_tracker.get_task.return_value = None

        with pytest.raises(TaskError, match=r"Task \d does not exist."):
            _ = TaskCmd(session).get_task(1)

    def test_show_tasks(self, session, printer):
        tasks = [Task("foo"), Task("bar")]
        session._daily_tracker.get_tasks.return_value = tasks

        TaskCmd(session).show_tasks()

        session._daily_tracker.get_tasks.assert_called_once_with(exclude=[])
        printer.echo.assert_called_once()
        printer.progress_bar.assert_not_called()

    def test_show_tasks_with_progress_bar(self, session, printer):
        tasks = [Task("foo"), Task("bar")]
        session._daily_tracker.get_tasks.return_value = tasks

        TaskCmd(session).show_tasks(progress_bar=True)

        session._daily_tracker.get_tasks.assert_called_once_with(exclude=[])
        printer.echo.assert_called_once()
        printer.progress_bar.assert_called_once_with(tasks)

    def test_show_tasks_fails(self, session, printer):
        session._daily_tracker.get_tasks.return_value = []

        with pytest.raises(HyperfocusExit):
            TaskCmd(session).show_tasks()

        printer.echo.assert_called_once_with("No tasks for today...")

    def test_ask_task_id(self, session, printer, prompt):
        tasks = [Task("foo"), Task("bar")]
        session._daily_tracker.get_tasks.return_value = tasks

        TaskCmd(session).ask_task_id("Test")

        printer.echo.assert_called_once()
        prompt.prompt.assert_called_once()

    def test_check_task_id_or_ask(self, mocker, session, printer, prompt):
        tasks = [Task("foo"), Task("bar")]
        session._daily_tracker.get_tasks.return_value = tasks
        prompt.prompt.return_value = mocker.sentinel.task_id

        task_id = TaskCmd(session).check_task_id_or_ask(None, "Test")

        assert task_id == mocker.sentinel.task_id
        printer.echo.assert_called_once()
        prompt.prompt.assert_called_once()

    def test_check_task_id_or_ask_with_id(self, session, prompt):
        task_id = TaskCmd(session).check_task_id_or_ask(1, "Test")

        assert task_id == 1
        prompt.prompt.assert_not_called()


class TestAddTaskCmd:
    def test_update_task_cmd(self, session, printer, formatter, prompt):
        session._daily_tracker.add_task.return_value = Task(
            id=1, title="foo", details="bar"
        )

        AddTaskCmd(session).execute(title="Test", add_details=False)

        prompt.prompt.assert_not_called()
        formatter.task.assert_called_once()
        printer.success.assert_called_once()

    def test_update_task_cmd_with_details(self, session, printer, formatter, prompt):
        session._daily_tracker.add_task.return_value = Task(
            id=1, title="foo", details="bar"
        )

        AddTaskCmd(session).execute(title="Test", add_details=True)

        prompt.prompt.assert_called_once_with("Task details")
        formatter.task.assert_called_once()
        printer.success.assert_called_once()


class TestUpdateTasksCmd:
    def test_update_tasks_cmd(self, mocker, session, printer, formatter):
        task1 = Task(id=1, title="foo", details="bar")
        task2 = Task(id=2, title="oof", details="rab")
        session._daily_tracker.get_task.side_effect = [task1, task2]

        UpdateTasksCmd(session).execute(
            task_ids=(1, 2), status=TaskStatus.DONE, text="Test"
        )

        session._daily_tracker.get_tasks.assert_not_called()
        session._daily_tracker.get_task.call_args_list = [
            mocker.call(1),
            mocker.call(2),
        ]
        session._daily_tracker.update_task.call_args_list = [
            mocker.call(task=task1, status=TaskStatus.DONE),
            mocker.call(task=task2, status=TaskStatus.DONE),
        ]
        assert formatter.task.call_count == 2
        assert printer.success.call_count == 2

    def test_update_tasks_cmd_ask_for_id_if_none(
        self, session, printer, formatter, prompt
    ):
        task = Task(id=1, title="foo", details="bar")
        session._daily_tracker.get_task.return_value = task

        UpdateTasksCmd(session).execute(
            task_ids=tuple(), status=TaskStatus.DONE, text="Test"
        )

        session._daily_tracker.get_tasks(exclude=[TaskStatus.DONE])
        prompt.prompt.assert_called_once()

    def test_update_tasks_cmd_with_same_status(self, session, printer, formatter):
        task = Task(id=1, title="foo", details="bar", status=TaskStatus.DELETED)
        session._daily_tracker.get_task.return_value = task

        UpdateTasksCmd(session).execute(
            task_ids=(1,), status=TaskStatus.DELETED, text="Test"
        )

        session._daily_tracker.get_tasks.assert_not_called()
        session._daily_tracker.get_task.assert_called_once_with(task_id=1)
        formatter.task.assert_called_once()
        printer.warning.assert_called_once()
        session._daily_tracker.update_task.assert_not_called()


class TestListTaskCmd:
    def test_list_task_cmd(self, session, printer):
        tasks = [Task("foo"), Task("bar")]
        session._daily_tracker.get_tasks.return_value = tasks

        ListTaskCmd(session).execute()

        session._daily_tracker.get_tasks.assert_called_once_with(exclude=[])
        printer.echo.assert_called_once()


class TestShowTaskCmd:
    def test_show_task_cmd(self, session, printer, prompt):
        task = Task(id=1, title="foo", details="bar")
        session._daily_tracker.get_task.return_value = task
        ShowTaskCmd(session).execute(task_id=1)

        prompt.prompt.assert_not_called()
        printer.task_details.assert_called_once_with(task)

    def test_show_task_cmd_ask_for_id_if_none(self, session, printer, prompt):
        task = Task(id=1, title="foo", details="bar")
        session._daily_tracker.get_task.return_value = task

        ShowTaskCmd(session).execute(task_id=None)

        prompt.prompt.assert_called_once()


class TestCopyCmd:
    def test_copy_task_details_cmd(self, session, printer, pyperclip):
        task = Task(id=1, title="foo", details="bar")
        session._daily_tracker.get_task.return_value = task

        CopyTaskDetailsCmd(session).execute(task_id=1)

        pyperclip.copy.assert_called_once_with("bar")
        printer.success.assert_called_once_with(
            "Task 1 details copied to clipboard.", event="success"
        )

    def test_copy_task_details_cmd_fails(self, session, printer, pyperclip):
        task = Task(id=1, title="foo", details="")
        session._daily_tracker.get_task.return_value = task

        with pytest.raises(TaskError, match=r"Task \d does not have details."):
            CopyTaskDetailsCmd(session).execute(task_id=1)

        pyperclip.copy.assert_not_called()
        printer.success.assert_not_called()

    def test_copy_task_details_cmd_ask_for_id_if_none(
        self, session, printer, pyperclip, prompt
    ):
        task = Task(id=1, title="foo", details="bar")
        session._daily_tracker.get_task.return_value = task

        CopyTaskDetailsCmd(session).execute(task_id=None)

        prompt.prompt.assert_called_once()
