from click.testing import CliRunner

from hyperfocus.termui import icons


runner = CliRunner()


def test_status(cli):
    result = runner.invoke(cli, ["status"])

    assert result.exit_code == 0
    assert result.output == "No tasks found...\n"

    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["add", "bar"])
    runner.invoke(cli, ["add", "baz"])
    runner.invoke(cli, ["done", "3"])

    result = runner.invoke(cli, ["status"])

    expected = (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        "  1   ⬢ foo      □     \n"
        "  2   ⬢ bar      □     \n"
        "  3   ⬢ baz      □     \n"
        "\n"
        f" {icons.TASK_STATUS} 33% [{icons.PROGRESSBAR * 10}"
        f"{icons.PROGRESSBAR_EMPTY * 20}]\n"
        "\n"
    )
    assert result.exit_code == 0
    assert result.output == expected
