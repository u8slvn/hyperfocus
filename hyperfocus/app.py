import functools
import sys

import typer

from hyperfocus import __app_name__
from hyperfocus.exceptions import HyperfocusException


def app_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HyperfocusException as error:
            typer.secho(str(error), fg=typer.colors.RED)
            raise typer.Exit(1)
        except typer.Exit as error:
            sys.exit(error.exit_code)
        except Exception as error:
            typer.secho(str(error), fg=typer.colors.RED)
            raise typer.Exit(1)

    return wrapper


class HyperfocusTyper(typer.Typer):
    def __call__(self, *args, **kwargs):
        super().__call__(prog_name=__app_name__, *args, **kwargs)

    def command(self, *args, **kwargs):
        def wrapper(func):
            func = app_error_handler(func)
            return super(HyperfocusTyper, self).command(*args, **kwargs)(func)

        return wrapper

    def callback(self, *args, **kwargs):
        def wrapper(func):
            func = app_error_handler(func)
            return super(HyperfocusTyper, self).callback(*args, **kwargs)(func)

        return wrapper
