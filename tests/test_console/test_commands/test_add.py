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
    result = runner.invoke(cli, ["add", "foo", "-d", "-"], input="bar\n")

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) " f"Task: #1 {icons.TASK_STATUS} foo created\n"
    )
