from pathlib import Path

import pytest
from freezegun import freeze_time
from typer.testing import CliRunner

from hyperfocus import __app_name__, __version__
from hyperfocus.cli import hyperfocus_app
from tests.conftest import pytest_regex

runner = CliRunner()


def test_main_cmd_version(cli_config):
    result = runner.invoke(hyperfocus_app, ["--version"])

    expected = f"{__app_name__} version {__version__}\n"
    assert expected == result.stdout


@pytest.mark.dependency()
@freeze_time("2012-12-21")
def test_call_main_cmd_without_init(cli_config):
    result = runner.invoke(hyperfocus_app, [])

    assert result.stdout == "Config does not exist, please run init command first\n"
    assert result.exit_code == 1


@pytest.mark.dependency()
@freeze_time("2012-12-21")
def test_init_cmd(cli_config, tmp_test_dir):
    db_test_path = Path(str(tmp_test_dir)) / "db_test.sqlite"

    result = runner.invoke(hyperfocus_app, ["init"], input=f"{db_test_path}\n")

    pattern = pytest_regex(
        r"\? Database location \[(.*)\]: (.*)\n"
        r"ℹ\(init\) Config file created successfully in (.*)\n"
        r"ℹ\(init\) Database initialized successfully in (.*)\n"
    )
    assert pattern == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_init_cmd"])
@freeze_time("2012-12-21")
def test_main_cmd_with_no_tasks(cli_config):
    result = runner.invoke(hyperfocus_app, [])

    expected = (
        "✨ Fri, 21 December 2012\n"
        "✨ A new day starts, good luck!\n\n"
        "No tasks yet for today...\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_init_cmd"])
@freeze_time("2012-12-21")
def test_add_task_cmd(cli_config):
    result = runner.invoke(hyperfocus_app, ["add"], input="Test\nTest\n")

    expected = (
        "? Task title: Test\n"
        "? Task description (optional): Test\n"
        "✔(created) Task #1 ⬢ Test ⊕\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_add_task_cmd"])
@freeze_time("2012-12-21")
def test_main_cmd_with_tasks(cli_config):
    result = runner.invoke(hyperfocus_app, [])

    expected = "  #  tasks\n---  --------\n  1  ⬢ Test ⊕ \n"
    assert result.stdout == expected
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_add_task_cmd"])
@freeze_time("2012-12-21")
def test_done_task_cmd(cli_config):
    result = runner.invoke(hyperfocus_app, ["done", "1"])

    expected = "✔(updated) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_add_task_cmd"])
@freeze_time("2012-12-21")
def test_done_non_existing_task_cmd(cli_config):
    result = runner.invoke(hyperfocus_app, ["done", "9"])

    expected = "✘(not found) Task id does not exist\n"
    assert expected == result.stdout
    assert result.exit_code == 1


@pytest.mark.dependency(depends=["test_add_task_cmd"])
@freeze_time("2012-12-21")
def test_reset_task_cmd(cli_config):
    result = runner.invoke(hyperfocus_app, ["reset", "1"])

    expected = "✔(updated) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_reset_task_cmd"])
@freeze_time("2012-12-21")
def test_reset_task_cmd_second_time(cli_config):
    result = runner.invoke(hyperfocus_app, ["reset", "1"])

    expected = "▼(no change) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_add_task_cmd"])
@freeze_time("2012-12-21")
def test_block_task_cmd(cli_config):
    result = runner.invoke(hyperfocus_app, ["block", "1"])

    expected = "✔(updated) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_add_task_cmd"])
@freeze_time("2012-12-21")
def test_delete_task_cmd(cli_config):
    result = runner.invoke(hyperfocus_app, ["delete", "1"])

    expected = "✔(updated) Task #1 ⬢ Test ⊕\n"
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_delete_task_cmd"])
@freeze_time("2012-12-21")
def test_main_cmd_with_deleted_task(cli_config):
    result = runner.invoke(hyperfocus_app, [])

    expected = "No tasks yet for today...\n"
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_add_task_cmd"])
@freeze_time("2012-12-21")
def test_update_task_with_no_id_cmd(cli_config):
    result = runner.invoke(hyperfocus_app, ["reset"], input="1")

    expected = (
        "  #  tasks\n"
        "---  --------\n"
        "  1  ⬢ Test ⊕ \n\n"
        "? Reset task: 1\n"
        "✔(updated) Task #1 ⬢ Test ⊕\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_add_task_cmd"])
@freeze_time("2012-12-21")
def test_show_task_cmd(cli_config):
    result = runner.invoke(hyperfocus_app, ["show", "1"])

    expected = "Task: #1 ⬢ Test\n" "Test\n"
    assert expected == result.stdout
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_add_task_cmd"])
@freeze_time("2012-12-21")
def test_show_task_with_no_id_cmd(cli_config):
    result = runner.invoke(hyperfocus_app, ["show"], input="1")

    expected = (
        "  #  tasks\n"
        "---  --------\n"
        "  1  ⬢ Test ⊕ \n\n"
        "? Show task details: 1\n"
        "Task: #1 ⬢ Test\n"
        "Test\n"
    )
    assert expected == result.stdout
    assert result.exit_code == 0
