import functools
import re

import click

from hyperfocus import printer
from hyperfocus.exceptions import HyperfocusException
from hyperfocus.utils import wrap_methods


def app_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HyperfocusException as error:
            printer.error(text=error.message, event=error.event)
            raise click.exceptions.Exit(1)
        except click.ClickException as error:
            message = error.format_message().rstrip(".")
            split_error_name = re.findall(r"[A-Z][^A-Z]*", type(error).__name__)
            event = " ".join(split_error_name).lower()
            printer.error(text=message, event=event)

    return wrapper


@wrap_methods(app_error_handler, ["make_context", "invoke"])
class Hyperfocus(click.Group):
    pass
