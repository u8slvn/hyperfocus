from __future__ import annotations

import pytest

from click.testing import CliRunner
from freezegun import freeze_time

from hyperfocus import __app_name__
from hyperfocus import __version__
from hyperfocus.termui import icons
from hyperfocus.termui.components import ProgressBar


runner = CliRunner()


@pytest.mark.functional
def test_hyf_version(cli):
    result = runner.invoke(cli, ["--version"])

    expected = f"{__app_name__}, version {__version__}\n"
    assert expected == result.stdout


@pytest.mark.functional
def test_hyf(cli_new_day):
    with freeze_time("2022-01-01"):
        result = runner.invoke(cli_new_day, [])

        expected = (
            "> ✨ Sat, 01 January 2022: A new day starts, good luck!\n"
            "No tasks for today...\n"
        )
        assert result.exit_code == 0
        assert result.output == expected

        runner.invoke(cli_new_day, ["add", "foo"])
        runner.invoke(cli_new_day, ["add", "bar"])
        runner.invoke(cli_new_day, ["add", "baz"])
        runner.invoke(cli_new_day, ["add", "qux"])
        runner.invoke(cli_new_day, ["done", "3"])

        result = runner.invoke(cli_new_day, [])

        expected = (
            "\n"
            "  #   tasks   details  \n"
            " --------------------- \n"
            "  1   ⬢ foo     [ ]    \n"
            "  2   ⬢ bar     [ ]    \n"
            "  3   ⬢ baz     [ ]    \n"
            "  4   ⬢ qux     [ ]    \n"
            "\n"
            f" {icons.TASK_STATUS} 25% [{icons.PROGRESSBAR * 8}"
            f"{icons.PROGRESSBAR_EMPTY * 22}]\n"
            "\n"
        )
        assert result.exit_code == 0
        assert result.output == expected

    with freeze_time("2022-01-02"):
        result = runner.invoke(cli_new_day, ["status"])

        expected = (
            "> ✨ Sun, 02 January 2022: A new day starts, good luck!\n"
            "> You have 3 unfinished task(s) from Sat, 01 January 2022, run 'hyf' "
            "to review.\n"
            "No tasks for today...\n"
        )
        assert result.exit_code == 0
        assert result.output == expected

        result = runner.invoke(cli_new_day, [], input="y\ny\nn\n\n")

        expected = (
            "? Review 3 unfinished task(s) from Sat, 01 January 2022 [Y/n]: y\n"
            '? Continue "foo" [Y/n]: y\n'
            '? Continue "bar" [Y/n]: n\n'
            '? Continue "qux" [Y/n]: \n'
            "\n"
            "  #   tasks   details  \n"
            " --------------------- \n"
            "  1   ⬢ foo     [ ]    \n"
            "  2   ⬢ qux     [ ]    \n"
            "\n"
            f" {icons.TASK_STATUS} 0% [{icons.PROGRESSBAR_EMPTY * ProgressBar.width}]\n"
            "\n"
        )
        assert result.exit_code == 0
        assert result.output == expected
