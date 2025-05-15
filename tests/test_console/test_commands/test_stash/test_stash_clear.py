from __future__ import annotations

from click.testing import CliRunner

from hyperfocus.termui import icons


runner = CliRunner()


def test_stash_clear(cli):
    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["add", "bar"])
    runner.invoke(cli, ["add", "foobar"])
    runner.invoke(cli, ["stash", "1", "2"])

    result = runner.invoke(cli, ["stash", "list"])

    assert result.exit_code == 0
    assert result.output == (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        f"  1   {icons.TASK_STATUS} foo     {icons.NO_DETAILS}    \n"
        f"  2   {icons.TASK_STATUS} bar     {icons.NO_DETAILS}    \n"
        "\n"
    )

    result = runner.invoke(cli, ["stash", "clear"])

    assert result.exit_code == 0
    assert result.output == "✔(success) Stash box cleared.\n"

    result = runner.invoke(cli, ["stash", "list"])

    assert result.exit_code == 0
    assert result.output == "No tasks in stash box...\n"

    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert result.output == (
        "\n"
        "  #   tasks      details  \n"
        " ------------------------ \n"
        f"  3   {icons.TASK_STATUS} foobar     {icons.NO_DETAILS}    \n"
        "\n"
        " ⬢ 0% [▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯]\n"
        "\n"
    )
