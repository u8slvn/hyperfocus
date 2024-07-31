from __future__ import annotations

import pytest

from click.testing import CliRunner

from hyperfocus.termui import icons


runner = CliRunner()


@pytest.mark.functional
def test_add(cli):
    result = runner.invoke(cli, ["add", "foo"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) " f"Task: #1 {icons.TASK_STATUS} foo created\n"
    )

    result = runner.invoke(cli, ["add", "bar", "-d"], input="baz\n")

    assert result.exit_code == 2


@pytest.mark.functional
def test_add_with_inline_details(cli):
    result = runner.invoke(cli, ["add", "foo", "-d", "bar"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) " f"Task: #1 {icons.TASK_STATUS} foo created\n"
    )


@pytest.mark.functional
def test_add_with_multiple_lines_details(mocker, cli):
    mocker.patch("click.edit", return_value="foo\nbar")
    result = runner.invoke(cli, ["add", "foo", "-d", "-"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) " f"Task: #1 {icons.TASK_STATUS} foo created\n"
    )


@pytest.mark.functional
def test_add_with_bulk_option(mocker, cli):
    mocker.patch("click.edit", return_value="foo\nbar")
    result = runner.invoke(cli, ["add", "-b"], input="bar\n")

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) Task: #1 {icons.TASK_STATUS} foo created\n"
        f"{icons.SUCCESS}(success) Task: #2 {icons.TASK_STATUS} bar created\n"
    )


@pytest.mark.functional
def test_add_with_bulk_option_ignore_empty_lines(mocker, cli):
    mocker.patch("click.edit", return_value="   \n\n \ntask n1\n \n\t\ntask n2")
    result = runner.invoke(cli, ["add", "-b"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) Task: #1 {icons.TASK_STATUS} task n1 created\n"
        f"{icons.SUCCESS}(success) Task: #2 {icons.TASK_STATUS} task n2 created\n"
    )


@pytest.mark.functional
def test_add_with_bulk_option_does_nothing_with_empty_lines(mocker, cli):
    mocker.patch("click.edit", return_value="   \n\n \n   \n")
    result = runner.invoke(cli, ["add", "-b"])

    assert result.exit_code == 0
    assert result.output == ""
