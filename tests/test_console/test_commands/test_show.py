import pytest
from click.testing import CliRunner
from freezegun import freeze_time

from hyperfocus.termui import icons
from tests.conftest import pytest_regex


runner = CliRunner()


@pytest.mark.functional
@freeze_time("2022-01-01")
def test_show(cli):
    result = runner.invoke(cli, ["show"])

    assert result.exit_code == 0
    assert result.output == "No tasks for today...\n"

    runner.invoke(cli, ["add", "foo"])

    result = runner.invoke(cli, ["show"], input="2\n")

    expected = (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        f"  1   {icons.TASK_STATUS} foo      {icons.NO_DETAILS}     \n"
        "\n"
        f"{icons.PROMPT} Show task details: 2\n"
        f"{icons.ERROR}(error) "
        f"Task 2 does not exist.\n"
    )
    assert result.exit_code == 1
    assert result.output == expected

    result = runner.invoke(cli, ["show", "1"])

    expected = pytest_regex(
        "Task: #1\n"
        f"Status: {icons.TASK_STATUS} Todo\n"
        "Title: foo\n"
        "Details: ...\n"
        "History: \n"
        " • (.*) - add task\n"
    )
    assert result.exit_code == 0
    assert expected == result.output
