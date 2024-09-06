from __future__ import annotations

import pytest

from click.testing import CliRunner

from hyperfocus.termui import icons


runner = CliRunner()


@pytest.fixture
def mock_click_edit(mocker):
    """Click edit mock.

    Simulates the click.edit function by replacing the first line of the input with the
    values in the replace_values list.
    """

    class MockEdit:
        def __init__(self, side_effect: list[str | None]):
            self.side_effect = iter(side_effect)

        def __call__(self, value):
            effect = next(self.side_effect)

            if effect is None:
                # If the replacement value is None, return the original value.
                return effect

            lines = value.split("\n")
            lines[0] = effect
            return "\n".join(lines)

    def configure_edit_mock(side_effect: list[str | None]):
        mocker.patch("click.edit", new_callable=MockEdit, side_effect=side_effect)

    return configure_edit_mock


@pytest.mark.functional
def test_edit(mock_click_edit, cli):
    result = runner.invoke(cli, ["edit"])

    assert result.exit_code == 0
    assert result.output == "No tasks for today...\n"

    runner.invoke(cli, ["add", "foo"])

    result = runner.invoke(cli, ["edit"], input="12\n")

    expected = (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        f"  1   {icons.TASK_STATUS} foo      {icons.NO_DETAILS}     \n"
        "\n"
        f"{icons.PROMPT} Edit task(s): 12\n"
        f"{icons.ERROR}(error) Task 12 does not exist.\n"
    )
    assert result.exit_code == 1
    assert result.output == expected

    mock_click_edit(["foobar", "foobaz"])

    result = runner.invoke(cli, ["edit", "1"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) Task: #1 {icons.TASK_STATUS} foobar edited.\n"
    )

    mock_click_edit([None])

    result = runner.invoke(cli, ["edit", "1", "-t"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.WARNING}(warning) Task: #1 {icons.TASK_STATUS} foobar unchanged.\n"
    )

    mock_click_edit(["foobaz foo"])

    result = runner.invoke(cli, ["edit", "1", "-d"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) Task: #1 {icons.TASK_STATUS} foobar edited.\n"
    )

    mock_click_edit(["foo", "bar"])

    result = runner.invoke(cli, ["edit", "1", "-t", "-d"])

    assert result.exit_code == 0
    assert result.output == (
        f"{icons.SUCCESS}(success) Task: #1 {icons.TASK_STATUS} foo edited.\n"
    )
