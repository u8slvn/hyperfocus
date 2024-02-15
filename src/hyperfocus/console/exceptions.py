from __future__ import annotations

import click

from hyperfocus.exceptions import HyperfocusError


class TaskError(HyperfocusError):
    pass


class HyperfocusExit(click.exceptions.Exit):
    pass
