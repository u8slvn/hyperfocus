from click.testing import CliRunner


def test_hyperfocus_main(mocker):
    test_cli = mocker.patch("hyperfocus.cli.cli")
    from hyperfocus import __main__ as hyperfocus

    mocker.patch.object(hyperfocus, "__name__", "__main__")

    hyperfocus.main()

    test_cli.assert_called_once()


runner = CliRunner()


def test_hyperfocus_handle_errors(hyperfocus_cli):
    result = runner.invoke(hyperfocus_cli, [])

    expected = "✘(error) Dummy group error\n"
    assert expected == result.output


def test_hyperfocus_command_handle_errors(hyperfocus_cli):
    result = runner.invoke(hyperfocus_cli, ["bar"])

    expected = "✘(foo) Dummy command error\n"
    assert expected == result.output
