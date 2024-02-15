from __future__ import annotations

from click.testing import CliRunner
from hyperfocus.termui import icons


runner = CliRunner()


def test_stash_pop_with_id(cli):
    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["stash", "push", "1"])

    result = runner.invoke(cli, ["stash", "pop", "1"])

    assert result.exit_code == 0
    assert result.output == "✔(success) Task: #1 ⬢ foo added from stash box.\n"


def test_stash_pop_fails_with_wrong_id(cli):
    result = runner.invoke(cli, ["stash", "pop", "11"])

    assert result.exit_code == 1
    assert result.output == "✘(error) Task 11 does not exist in stash box.\n"


def test_stash_pop_with_no_task_in_stash_box(cli):
    result = runner.invoke(cli, ["stash", "pop"])

    assert result.exit_code == 0
    assert result.output == "No tasks in stash box...\n"


def test_stash_pop_with_ids(cli):
    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["add", "bar"])
    runner.invoke(cli, ["stash", "push", "1", "2"])

    result = runner.invoke(cli, ["stash", "pop", "1", "2"])

    assert result.exit_code == 0
    assert result.output == (
        "✔(success) Task: #1 ⬢ foo added from stash box.\n"
        "✔(success) Task: #2 ⬢ bar added from stash box.\n"
    )


def test_stash_add_without_id(cli):
    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["stash", "push", "1"])

    result = runner.invoke(cli, ["stash", "pop"], input="1\n")

    assert result.exit_code == 0
    assert result.output == (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        f"  1   {icons.TASK_STATUS} foo      {icons.NO_DETAILS}     \n"
        "\n"
        "? Stash task: 1\n"
        "✔(success) Task: #1 ⬢ foo added from stash box.\n"
    )
