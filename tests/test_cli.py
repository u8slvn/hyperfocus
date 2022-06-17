from datetime import datetime

from click.testing import CliRunner

from hyperfocus import __app_name__, __version__
from hyperfocus.cli import cli
from hyperfocus.models import Status, Task
from tests.conftest import pytest_regex

runner = CliRunner()


def test_main_cmd_version():
    result = runner.invoke(cli, ["--version"])

    expected = f"{__app_name__}, version {__version__}\n"
    assert expected == result.stdout


#
# def test_call_main_cmd_without_init(cli_config):
#     result = runner.invoke(cli, [])
#
#     assert result.stdout == "Config does not exist, please run init command first\n"
#     assert result.exit_code == 1


def test_init_cmd(tmp_test_dir):
    db_test_path = tmp_test_dir / "test_db.sqlite"

    result = runner.invoke(cli, ["init"], input=f"{db_test_path}\n")

    pattern = pytest_regex(
        r"\? Database location \[(.*)\]: (.*)\n"
        r"ℹ\(init\) Config file created successfully in (.*)\n"
        r"ℹ\(init\) Database initialized successfully in (.*)\n"
    )
    assert pattern == result.stdout
    assert result.exit_code == 0


def test_main_cmd_with_no_tasks(cli_session):
    cli_session.is_a_new_day.return_value = True
    cli_session.date = datetime(2012, 12, 21, 0, 0)
    cli_session.daily_tracker_service.get_tasks.return_value = []

    result = runner.invoke(cli, [])

    expected = (
        "✨ Fri, 21 December 2012\n"
        "✨ A new day starts, good luck!\n\n"
        "No tasks yet for today...\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0


def test_add_task_cmd(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker_service.add_task.return_value = task

    result = runner.invoke(cli, ["add"], input="Test\nTest\n")

    expected = (
        "? Task title: Test\n"
        "? Task details (optional): Test\n"
        "✔(created) Task #1 ⬢ Test ⊕\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0


def test_main_cmd_with_tasks(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker_service.get_tasks.return_value = [task]

    result = runner.invoke(cli, [])

    expected = "  #  tasks\n---  --------\n  1  ⬢ Test ⊕ \n"
    assert result.stdout == expected
    assert result.exit_code == 0


def test_done_task_cmd(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker_service.get_task.return_value = task

    result = runner.invoke(cli, ["done", "1"])

    expected = "✔(updated) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker_service.update_task.assert_called_once_with(
        status=Status.DONE, task=task
    )


def test_done_non_existing_task_cmd(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker_service.get_task.return_value = None

    result = runner.invoke(cli, ["done", "9"])

    expected = "✘(not found) Task id does not exist\n"
    assert expected == result.stdout
    assert result.exit_code == 1
    cli_session.daily_tracker_service.update_task.assert_not_called()


def test_reset_task_cmd(cli_session):
    task = Task(id=1, title="Test", details="Test", status=Status.DONE.value)
    cli_session.daily_tracker_service.get_task.return_value = task

    result = runner.invoke(cli, ["reset", "1"])

    expected = "✔(updated) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker_service.update_task.assert_called_once_with(
        status=Status.TODO, task=task
    )


def test_reset_task_cmd_on_already_reset_task(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker_service.get_task.return_value = task

    result = runner.invoke(cli, ["reset", "1"])

    expected = "▼(no change) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker_service.update_task.assert_not_called()


def test_block_task_cmd(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker_service.get_task.return_value = task

    result = runner.invoke(cli, ["block", "1"])

    expected = "✔(updated) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker_service.update_task.assert_called_once_with(
        status=Status.BLOCKED, task=task
    )


def test_delete_task_cmd(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker_service.get_task.return_value = task

    result = runner.invoke(cli, ["delete", "1"])

    expected = "✔(updated) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker_service.update_task.assert_called_once_with(
        status=Status.DELETED, task=task
    )


def test_main_cmd_with_deleted_task(cli_session):
    cli_session.daily_tracker_service.get_tasks.return_value = []

    result = runner.invoke(cli, [])

    expected = "No tasks yet for today...\n"
    assert expected == result.stdout
    assert result.exit_code == 0


def test_update_task_with_no_id_cmd(cli_session):
    task = Task(id=1, title="Test", details="Test", status=Status.DONE.value)
    cli_session.daily_tracker_service.get_tasks.return_value = [task]
    cli_session.daily_tracker_service.get_task.return_value = task

    result = runner.invoke(cli, ["reset"], input="1")

    expected = (
        "  #  tasks\n"
        "---  --------\n"
        "  1  ⬢ Test ⊕ \n\n"
        "? Reset task: 1\n"
        "✔(updated) Task #1 ⬢ Test ⊕\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0
    cli_session.daily_tracker_service.update_task.assert_called_once_with(
        status=Status.TODO, task=task
    )


def test_show_task_cmd(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker_service.get_task.return_value = task

    result = runner.invoke(cli, ["show", "1"])

    expected = "Task: #1 ⬢ Test\n" "Test\n"
    assert expected == result.stdout
    assert result.exit_code == 0


def test_show_task_with_no_id_cmd(cli_session):
    task = Task(id=1, title="Test", details="Test")
    cli_session.daily_tracker_service.get_tasks.return_value = [task]
    cli_session.daily_tracker_service.get_task.return_value = task

    result = runner.invoke(cli, ["show"], input="1")

    expected = (
        "  #  tasks\n"
        "---  --------\n"
        "  1  ⬢ Test ⊕ \n\n"
        "? Show task details: 1\n"
        "Task: #1 ⬢ Test\n"
        "Test\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0
