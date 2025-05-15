from __future__ import annotations

from click.testing import CliRunner

from hyperfocus.termui import icons


runner = CliRunner()


def test_stash_list(cli):
    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["add", "bar"])
    runner.invoke(cli, ["stash", "1", "2"])

    result = runner.invoke(cli, ["stash", "apply"])

    assert result.exit_code == 0
    assert result.output == "✔(success) All tasks in stash box added for today.\n"

    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert result.output == (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        f"  3   {icons.TASK_STATUS} foo     {icons.NO_DETAILS}    \n"
        f"  4   {icons.TASK_STATUS} bar     {icons.NO_DETAILS}    \n"
        "\n"
        " ⬢ 0% [▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯]\n"
        "\n"
    )
