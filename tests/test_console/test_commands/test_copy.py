from click.testing import CliRunner


runner = CliRunner()


def test_copy(mocker, cli):
    pyperclip = mocker.patch("hyperfocus.console.commands.copy.pyperclip")

    result = runner.invoke(cli, ["copy"])

    assert result.exit_code == 0
    assert result.output == "No tasks for today...\n"

    runner.invoke(cli, ["add", "foo"])
    runner.invoke(cli, ["add", "bar", "-d"], input="foobar\n")

    result = runner.invoke(cli, ["copy"], input="1\n")

    expected = (
        "\n"
        "  #   tasks   details  \n"
        " --------------------- \n"
        "  1   ⬢ foo      □     \n"
        "  2   ⬢ bar      ■     \n"
        "\n"
        "? Copy task details: 1\n"
        "✘(task error) Task 1 does not have details.\n"
    )
    assert result.exit_code == 1
    assert result.output == expected

    result = runner.invoke(cli, ["copy", "77"])

    assert result.exit_code == 1
    assert result.output == "✘(task error) Task 77 does not exist.\n"

    result = runner.invoke(cli, ["copy", "2"])

    assert result.exit_code == 0
    assert result.output == "✔(success) Task 2 details copied to clipboard.\n"
    pyperclip.copy.assert_called_once_with("foobar")
