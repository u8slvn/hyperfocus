from __future__ import annotations

import pytest

from click.testing import CliRunner

from hyperfocus.termui import icons


runner = CliRunner()


@pytest.mark.functional
def test_reset(cli):
    result = runner.invoke(cli, ["reset"])

    assert result.exit_code == 0
    assert result.output == "No tasks for today...\n"

    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["done", "1"])

    result = runner.invoke(cli, ["reset"], input="12\n")

    expected = (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        f"  1   {icons.TASK_STATUS} foo      {icons.NO_DETAILS}     \n"
        "\n"
        f"{icons.PROMPT} Reset task(s): 12\n"
        f"{icons.ERROR}(error) Task 12 does not exist.\n"
    )
    assert result.exit_code == 1
    assert result.output == expected

    result = runner.invoke(cli, ["reset", "1"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) Task: #1 {icons.TASK_STATUS} foo reset.\n"
    )

    result = runner.invoke(cli, ["reset", "1"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.WARNING}(warning) Task: #1 {icons.TASK_STATUS} foo unchanged.\n"
    )
