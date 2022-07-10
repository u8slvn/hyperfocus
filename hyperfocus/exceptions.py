from __future__ import annotations

import click

from hyperfocus.utils import un_camel_case


class HyperfocusException(Exception):
    exit_code = 1

    def __init__(self, message: str, event: str | None = None):
        super().__init__(message)
        self._event = event
        self.message = message

    @property
    def event(self):
        if self._event:
            return self._event

        return un_camel_case(type(self).__name__)


class HyperfocusExit(click.exceptions.Exit):
    pass


class AliasError(HyperfocusException):
    pass


class TaskError(HyperfocusException):
    pass


class SessionError(HyperfocusException):
    pass


class ServiceError(HyperfocusException):
    pass
