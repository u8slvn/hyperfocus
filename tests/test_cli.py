from datetime import date

import pytest
from click.testing import CliRunner

from hyperfocus import __app_name__, __version__
from hyperfocus.cli import hyf
from hyperfocus.database.models import Task, TaskStatus
from hyperfocus.services import DailyTrackerService, NullDailyTrackerService
from tests.conftest import pytest_regex


runner = CliRunner()


def test_main_cmd_version():
    result = runner.invoke(hyf, ["--version"])

    expected = f"{__app_name__}, version {__version__}\n"
    assert expected == result.stdout


def test_init_cmd(mocker, test_dir, cli_session):
    db_path = test_dir / "test_database.sqlite"
    config_path = test_dir / "config.ini"
    mocker.patch("hyperfocus.config.config.CONFIG_PATH", config_path)

    result = runner.invoke(hyf, ["init"], input=f"{db_path}\n")

    pattern = pytest_regex(
        r"\? Database location \[(.*)\]: (.*)\n"
        r"ℹ\(init\) Config file created successfully in (.*)\n"
        r"ℹ\(init\) Database initialized successfully in (.*)\n"
    )
    assert pattern == result.stdout
    assert result.exit_code == 0


def test_new_day_without_previous_tasks_review(cli_session):
    cli_session.daily_tracker.new_day = True
    cli_session.daily_tracker.date = date(2012, 12, 21)
    cli_session.daily_tracker.get_tasks.return_value = []
    cli_session.past_tracker.get_previous_day.return_value = NullDailyTrackerService()

    result = runner.invoke(hyf, ["status"])

    expected = (
        "✨ Fri, 21 December 2012\n"
        "✨ A new day starts, good luck!\n\n"
        "No tasks for today...\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0


def test_status_cmd_with_previous_tasks_review(mocker, cli_session):
    task1 = Task(id=1, title="Test1", details="Test1")
    task2 = Task(id=2, title="Test2", details="Test2")
    cli_session.daily_tracker.new_day = True
    cli_session.daily_tracker.date = date(2012, 12, 21)
    cli_session.daily_tracker.get_tasks.return_value = [task1]
    previous_day = mocker.Mock(spec=DailyTrackerService)
    previous_day.date = date(2012, 12, 15)
    previous_day.get_tasks.return_value = [task1, task2]
    cli_session.past_tracker.get_previous_day.return_value = previous_day

    result = runner.invoke(hyf, ["status"], input="y\ny\nn\n")

    expected = (
        "✨ Fri, 21 December 2012\n"
        "✨ A new day starts, good luck!\n\n"
        "Unfinished task(s) from Sat, 15 December 2012:\n"
        "  #  tasks\n"
        "---  ---------\n"
        "  1  ⬢ Test1 ⊕\n"
        "  2  ⬢ Test2 ⊕ \n\n"
        "? Review 2 unfinished task(s) [Y/n]: y\n"
        '? Take back task "Test1" for today [y/N]: y\n'
        '? Take back task "Test2" for today [y/N]: n\n\n'
        "  #  tasks\n"
        "---  ---------\n"
        "  1  ⬢ Test1 ⊕ \n\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker.add_task.assert_called_once_with(
        title="Test1", details="Test1"
    )


def test_status_cmd_with_previous_tasks_review_dismiss(mocker, cli_session):
    task1 = Task(id=1, title="Test1", details="Test1")
    cli_session.daily_tracker.new_day = True
    cli_session.daily_tracker.date = date(2012, 12, 21)
    cli_session.daily_tracker.get_tasks.return_value = []
    previous_day = mocker.Mock(spec=DailyTrackerService)
    previous_day.date = date(2012, 12, 15)
    previous_day.get_tasks.return_value = [task1]
    cli_session.past_tracker.get_previous_day.return_value = previous_day

    result = runner.invoke(hyf, ["status"], input="n\n")

    expected = (
        "✨ Fri, 21 December 2012\n"
        "✨ A new day starts, good luck!\n\n"
        "Unfinished task(s) from Sat, 15 December 2012:\n"
        "  #  tasks\n"
        "---  ---------\n"
        "  1  ⬢ Test1 ⊕ \n\n"
        "? Review 1 unfinished task(s) [Y/n]: n\n"
        "No tasks for today...\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker.add_task.assert_not_called()


def test_status_cmd_without_task(cli_session):
    cli_session.daily_tracker.get_tasks.return_value = []

    result = runner.invoke(hyf, ["status"])

    expected = "No tasks for today...\n"
    assert expected == result.stdout
    assert result.exit_code == 0


def test_status_cmd_with_tasks(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker.get_tasks.return_value = [task]

    result = runner.invoke(hyf, ["status"])

    expected = "  #  tasks\n---  --------\n  1  ⬢ Test ⊕ \n\n"
    assert result.stdout == expected
    assert result.exit_code == 0


def test_add_cmd_task_without_details(cli_session):
    task = Task(id=1, title="Test")
    cli_session.daily_tracker.add_task.return_value = task

    result = runner.invoke(hyf, ["add", "Test"])

    expected = "✔(created) Task: #1 ⬢ Test ◌\n"
    assert expected == result.stdout
    assert result.exit_code == 0


def test_add_cmd_task_with_details(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker.add_task.return_value = task

    result = runner.invoke(hyf, ["add", "Test", "-d"], input="Test\n")

    expected = "? Task details: Test\n" "✔(created) Task: #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "command",
    [
        "delete",
        "done",
        "block",
        "reset",
    ],
)
def test_done_cmd_non_existing_task(cli_session, command):
    cli_session.daily_tracker.get_task.return_value = None

    result = runner.invoke(hyf, [command, "9"])

    expected = "✘(task error) Task 9 does not exist.\n"
    assert expected == result.stdout
    assert result.exit_code == 1
    cli_session.daily_tracker.update_task.assert_not_called()


def test_reset_cmd_task(cli_session):
    task = Task(id=1, title="Test", details="Test", status=TaskStatus.DONE)
    cli_session.daily_tracker.get_task.return_value = task

    result = runner.invoke(hyf, ["reset", "1"])

    expected = "✔(updated) Task: #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker.get_task.assert_called_once_with(task_id=1)
    cli_session.daily_tracker.update_task.assert_called_once_with(
        status=TaskStatus.TODO, task=task
    )


def test_reset_cmd_task_on_already_reset_task(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker.get_task.return_value = task

    result = runner.invoke(hyf, ["reset", "1"])

    expected = "▼(no change) Task: #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker.get_task.assert_called_once_with(task_id=1)
    cli_session.daily_tracker.update_task.assert_not_called()


@pytest.mark.parametrize(
    "command, updated",
    [
        ("delete", TaskStatus.DELETED),
        ("done", TaskStatus.DONE),
        ("block", TaskStatus.BLOCKED),
    ],
)
def test_update_status_cmd_task(cli_session, command, updated):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker.get_task.return_value = task

    result = runner.invoke(hyf, [command, "1"])

    expected = "✔(updated) Task: #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker.get_task.assert_called_once_with(task_id=1)
    cli_session.daily_tracker.update_task.assert_called_once_with(
        status=updated, task=task
    )


def test_update_task_with_no_id(cli_session):
    task = Task(id=1, title="Test", details="Test", status=TaskStatus.DONE.value)
    cli_session.daily_tracker.get_tasks.return_value = [task]
    cli_session.daily_tracker.get_task.return_value = task

    result = runner.invoke(hyf, ["reset"], input="1")

    expected = (
        "  #  tasks\n"
        "---  --------\n"
        "  1  ⬢ Test ⊕ \n\n"
        "? Reset task: 1\n"
        "✔(updated) Task: #1 ⬢ Test ⊕\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker.get_task.assert_called_once_with(task_id=1)
    cli_session.daily_tracker.update_task.assert_called_once_with(
        status=TaskStatus.TODO, task=task
    )
