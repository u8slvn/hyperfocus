import pytest
import typer
from typer.testing import CliRunner

from hyperfocus import cli
from hyperfocus.app import HyperfocusTyper


def test_hyperfocus_main(mocker):
    hyperfocus_app = mocker.Mock()
    mocker.patch.object(cli, "hyperfocus_app", hyperfocus_app)
    from hyperfocus import __main__ as hyperfocus

    mocker.patch.object(hyperfocus, "__name__", "__main__")

    hyperfocus.main()

    hyperfocus_app.assert_called_once()


@pytest.fixture(scope="session")
def hyperfocus_test():
    test_app = HyperfocusTyper()

    @test_app.command()
    def foo():
        raise Exception("Dummy command error")

    @test_app.callback(invoke_without_command=True)
    def bar(ctx: typer.Context):
        if ctx.invoked_subcommand is None:
            raise Exception("Dummy callback error")

    return test_app


def test_hyperfocus_typer_command_handle_errors(hyperfocus_test):
    runner = CliRunner()

    result = runner.invoke(hyperfocus_test, ["foo"])

    expected = "Dummy command error\n"
    assert expected == result.output


def test_hyperfocus_typer_callback_handle_errors(hyperfocus_test):
    runner = CliRunner()

    result = runner.invoke(hyperfocus_test, [])

    expected = "Dummy callback error\n"
    assert expected == result.output


def test_hyperfocus_typer_call(mocker, hyperfocus_test):
    typer_cli = mocker.patch("hyperfocus.app.typer.Typer.__call__")

    hyperfocus_test()

    typer_cli.assert_called_once_with(prog_name="hyperfocus")
