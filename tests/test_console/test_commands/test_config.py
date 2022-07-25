from click.testing import CliRunner

from tests.conftest import pytest_regex


runner = CliRunner()


def test_config(cli):
    result = runner.invoke(cli, ["config", "--list"])

    assert result.exit_code == 0
    assert pytest_regex("core.database = (.*)\n") == result.output

    result = runner.invoke(cli, ["config", "alias.st", "status"])

    assert result.exit_code == 0
    assert result.output == "✔(success) Config updated\n"

    result = runner.invoke(cli, ["config", "--list"])

    assert result.exit_code == 0
    assert pytest_regex("core.database = (.*)\n" "alias.st = status\n") == result.output

    result = runner.invoke(cli, ["config", "alias.st", "--unset"])

    assert result.exit_code == 0
    assert result.output == "✔(success) Config updated\n"

    result = runner.invoke(cli, ["config", "--list"])

    assert result.exit_code == 0
    assert pytest_regex("core.database = (.*)\n") == result.output
