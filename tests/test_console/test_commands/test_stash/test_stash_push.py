from click.testing import CliRunner

from hyperfocus.termui import icons


runner = CliRunner()


def test_stash_push_with_id(cli):
    runner.invoke(cli, ["add", "foo"])

    result = runner.invoke(cli, ["stash", "push", "1"])

    assert result.exit_code == 0
    assert result.output == "✔(success) Task: #1 ⬢ foo stashed.\n"


def test_stash_push_fails_with_wrong_id(cli):
    runner.invoke(cli, ["add", "foo"])

    result = runner.invoke(cli, ["stash", "push", "11"])

    assert result.exit_code == 1
    assert result.output == "✘(error) Task 11 does not exist.\n"


def test_stash_push_with_ids(cli):
    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["add", "bar"])

    result = runner.invoke(cli, ["stash", "push", "1", "2"])

    assert result.exit_code == 0
    assert result.output == (
        "✔(success) Task: #1 ⬢ foo stashed.\n" "✔(success) Task: #2 ⬢ bar stashed.\n"
    )


def test_stash_push_without_id(cli):
    runner.invoke(cli, ["add", "foo"])

    result = runner.invoke(cli, ["stash", "push"], input="1\n")

    assert result.exit_code == 0
    assert result.output == (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        f"  1   {icons.TASK_STATUS} foo      {icons.NO_DETAILS}     \n"
        "\n"
        "? Stash task: 1\n"
        "✔(success) Task: #1 ⬢ foo stashed.\n"
    )
