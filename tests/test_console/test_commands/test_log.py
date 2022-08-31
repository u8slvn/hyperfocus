from click.testing import CliRunner
from freezegun import freeze_time

from hyperfocus.termui import icons


runner = CliRunner()


def test_done(cli):
    with freeze_time("2022-01-01"):
        result = runner.invoke(cli, ["log"])

        assert result.exit_code == 0
        assert result.output == "\n"

        runner.invoke(cli, ["add", "foo"])
        runner.invoke(cli, ["add", "bar"])

    with freeze_time("2022-01-02"):
        runner.invoke(cli, ["add", "baz"])

    with freeze_time("2022-01-03"):
        result = runner.invoke(cli, ["log"])

        assert result.exit_code == 0
        assert result.output == (
            "> You have 1 unfinished task(s) from Sun, 02 January 2022,"
            " run 'hyf' to review.\n"
            f"{icons.LIST} Sun, 02 January 2022\n"
            f"{icons.HISTORY_END_NODE} ⬢ baz\n\n"
            f"{icons.LIST} Sat, 01 January 2022\n"
            f"{icons.HISTORY_NODE} ⬢ foo\n"
            f"{icons.HISTORY_END_NODE} ⬢ bar\n"
            "\n\n"
        )
