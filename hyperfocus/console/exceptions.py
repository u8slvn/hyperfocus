import click

from hyperfocus.exceptions import HyperfocusException


class TaskError(HyperfocusException):
    pass


class HyperfocusExit(click.exceptions.Exit):
    pass
