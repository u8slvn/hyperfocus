import click.exceptions
import pytest

from hyperfocus.exceptions import HyperfocusException, HyperfocusExit
from hyperfocus.hyf_click.error_handler import hyf_error_handler


def test_hyf_error_handler_catch_hyperfocus_exec(mocker):
    printer = mocker.patch("hyperfocus.hyf_click.error_handler.printer")

    @hyf_error_handler
    def foobar():
        raise HyperfocusException("Test exception.", event="error")

    with pytest.raises(HyperfocusExit):
        foobar()

    printer.error.assert_called_once_with(text="Test exception.", event="error")


def test_hyf_error_handler_catch_click_exec(mocker):
    printer = mocker.patch("hyperfocus.hyf_click.error_handler.printer")

    @hyf_error_handler
    def foobar():
        raise click.exceptions.ClickException("Test exception.")

    with pytest.raises(HyperfocusExit):
        foobar()

    printer.error.assert_called_once_with(
        text="Test exception.", event="click exception"
    )


def test_hyf_error_handler_catch_click_usage_error_exec(mocker):
    printer = mocker.patch("hyperfocus.hyf_click.error_handler.printer")
    click_ctx = mocker.Mock(spec=click.Context)
    click_ctx = click_ctx(mocker.sentinel.command)
    click_ctx.command = mocker.Mock(**{"get_help_option.return_value": True})
    click_ctx.command_path = "foo"
    click_ctx.help_option_names = ["bar"]
    click_ctx.get_usage.return_value = "Test usage."

    @hyf_error_handler
    def foobar():
        raise click.exceptions.UsageError("Test usage error", ctx=click_ctx)

    with pytest.raises(HyperfocusExit):
        foobar()

    printer.echo.assert_called_once_with("Test usage.\nTry 'foo bar' for help.\n")
    printer.error.assert_called_once_with(text="Test usage error.", event="usage error")
