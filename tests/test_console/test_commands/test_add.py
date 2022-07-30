from click.testing import CliRunner

from hyperfocus.termui import icons


runner = CliRunner()


def test_add(cli):
    result = runner.invoke(cli, ["add", "foo"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.NOTIFICATION_SUCCESS}(created) " f"Task: #1 {icons.TASK_STATUS} foo\n"
    )

    result = runner.invoke(cli, ["add", "bar", "-d"], input="baz\n")

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.PROMPT} Task details: baz\n"
        f"{icons.NOTIFICATION_SUCCESS}(created) "
        f"Task: #2 {icons.TASK_STATUS} bar\n"
    )
