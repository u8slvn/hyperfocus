import pytest
from click.testing import CliRunner
from freezegun import freeze_time

from hyperfocus.termui import icons
from tests.conftest import pytest_regex


runner = CliRunner()


@pytest.mark.functional
@freeze_time("2022-01-01")
def test_config(cli):
    result = runner.invoke(cli, ["config", "--list"])

    assert result.exit_code == 0
    assert pytest_regex("core.database = (.*)\n") == result.output

    result = runner.invoke(cli, ["config", "alias.st", "status"])

    assert result.exit_code == 0
    assert result.output == f"{icons.SUCCESS}(success) Config updated\n"

    result = runner.invoke(cli, ["config", "--list"])

    assert result.exit_code == 0
    assert (
        pytest_regex(
            "core.database = (.*)\ncore.force_color = (.*)\nalias.st = status\n"
        )
        == result.output
    )

    result = runner.invoke(cli, ["config", "alias.st", "--unset"])

    assert result.exit_code == 0
    assert result.output == f"{icons.SUCCESS}(success) Config updated\n"

    result = runner.invoke(cli, ["config", "--list"])

    assert result.exit_code == 0
    assert pytest_regex("core.database = (.*)\n") == result.output
