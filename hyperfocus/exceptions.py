from __future__ import annotations

import click


class HyperfocusException(Exception):
    exit_code = 1

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class HyperfocusExit(click.exceptions.Exit):
    pass


class TaskError(HyperfocusException):
    pass


class SessionError(HyperfocusException):
    pass
