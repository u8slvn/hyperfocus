from __future__ import annotations

from click.testing import CliRunner
from hyperfocus.termui import icons


runner = CliRunner()


def test_stash_list(cli):
    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["stash", "push", "1"])

    result = runner.invoke(cli, ["stash", "list"])

    assert result.exit_code == 0
    assert result.output == (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        f"  1   {icons.TASK_STATUS} foo      {icons.NO_DETAILS}     \n"
        "\n"
    )


def test_stash_list_without_stashed_tasks(cli):
    result = runner.invoke(cli, ["stash", "list"])

    assert result.exit_code == 0
    assert result.output == "No tasks in stash box...\n"
