from __future__ import annotations

import functools
from typing import Callable

import click

from hyperfocus.commands import printer
from hyperfocus.exceptions import HyperfocusException, HyperfocusExit
from hyperfocus.utils import un_camel_case


class HyfClickExceptionAdapter(HyperfocusException):
    def __init__(
        self, message: str, event: str, exit_code: int, msg_prefix: str | None = None
    ) -> None:
        super().__init__(message, event)
        self.exit_code = exit_code
        self.msg_prefix = msg_prefix

    @functools.singledispatchmethod
    @classmethod
    def adapt_from(
        cls, exception: click.exceptions.ClickException
    ) -> HyfClickExceptionAdapter:
        return cls(
            message=exception.format_message(),
            event=un_camel_case(type(exception).__name__),
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
            event=un_camel_case(type(exception).__name__),
            exit_code=exception.exit_code,
            msg_prefix=f"{usage}{hint}",
        )


def hyf_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        try:
            return func(*args, **kwargs)
        except HyperfocusException as error:
            printer.error(text=error.message, event=error.event)
            raise HyperfocusExit(error.exit_code)
        except click.ClickException as error:
            hyf_error = HyfClickExceptionAdapter.adapt_from(error)
            if hyf_error.msg_prefix:
                printer.echo(hyf_error.msg_prefix)
            printer.error(text=hyf_error.message, event=hyf_error.event)
            raise HyperfocusExit(error.exit_code)

    return wrapper
