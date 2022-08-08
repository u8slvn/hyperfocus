from __future__ import annotations

import functools
from typing import Any, Callable

import click

from hyperfocus.console.exceptions import HyperfocusExit
from hyperfocus.exceptions import HyperfocusException
from hyperfocus.termui import printer
from hyperfocus.termui.components import ErrorNotification


class HyfClickExceptionAdapter(HyperfocusException):
    def __init__(
        self, message: str, exit_code: int, msg_prefix: str | None = None
    ) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.msg_prefix = msg_prefix

    @functools.singledispatchmethod
    @classmethod
    def adapt_from(
        cls, exception: click.exceptions.ClickException
    ) -> HyfClickExceptionAdapter:
        return cls(
            message=exception.format_message(),
            exit_code=exception.exit_code,
        )

    @adapt_from.register(click.exceptions.UsageError)
    @classmethod
    def _(cls, exception: click.exceptions.UsageError) -> HyfClickExceptionAdapter:
        hint = ""
        usage = ""
        if (
            exception.ctx is not None
            and exception.ctx.command.get_help_option(exception.ctx) is not None
        ):
            command = exception.ctx.command_path
            option = exception.ctx.help_option_names[0]
            hint = f"Try '{command} {option}' for help.\n"
        if exception.ctx is not None:
            usage = f"{exception.ctx.get_usage()}\n"

        return cls(
            message=exception.format_message(),
            exit_code=exception.exit_code,
            msg_prefix=f"{usage}{hint}",
        )


def hyf_error_handler(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except HyperfocusException as error:
            printer.echo(ErrorNotification(text=error.message))
            raise HyperfocusExit(error.exit_code)
        except click.ClickException as error:
            hyf_error = HyfClickExceptionAdapter.adapt_from(error)
            if hyf_error.msg_prefix:
                printer.echo(hyf_error.msg_prefix)
            printer.echo(ErrorNotification(text=hyf_error.message))
            raise HyperfocusExit(error.exit_code)

    return wrapper
