from click.testing import CliRunner
from freezegun import freeze_time


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
            "\nSun, 02 January 2022\n"
            "  ⬢ baz\n"
            "\nSat, 01 January 2022\n"
            "  ⬢ foo\n"
            "  ⬢ bar\n"
            "\n"
        )
