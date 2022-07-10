from hyperfocus.commands.cmd_status import StatusCommand
from hyperfocus.commands.cmd_task import TaskCommand


def test_status_command(mocker, test_session):
    task_command = mocker.Mock(spec=TaskCommand, instance=True)
    mocker.patch(
        "hyperfocus.commands.cmd_status.TaskCommand", return_value=task_command
    )

    StatusCommand(test_session).execute()

    task_command.show_tasks.assert_called_once()
