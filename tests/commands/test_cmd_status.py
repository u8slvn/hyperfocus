import pytest

from hyperfocus.commands.cmd_status import StatusCommand
from hyperfocus.commands.cmd_task import TaskCommand


@pytest.fixture
def printer(mocker):
    yield mocker.patch("hyperfocus.commands.cmd_status.printer")


@pytest.fixture
def task_command(mocker):
    task_command = mocker.Mock(spec=TaskCommand, instance=True)
    mocker.patch(
        "hyperfocus.commands.cmd_status.TaskCommand", return_value=task_command
    )
    return task_command


def test_status_command(test_session, task_command):
    StatusCommand(test_session).execute()

    task_command.show_tasks.assert_called_once()
