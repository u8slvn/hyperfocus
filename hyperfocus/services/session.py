from __future__ import annotations

import datetime

import click

from hyperfocus.config.config import Config
from hyperfocus.database import database
from hyperfocus.services.daily_tracker import DailyTracker
from hyperfocus.services.exceptions import SessionError


class Session:
    """
    Manage the session of the whole CLI.

    A new session is created each time a command is called. It primarily handles
    database connexion and daily tracker service (which is the main service of
    the CLI).
    """

    _database = database

    def __init__(self, config: Config, daily_tracker: DailyTracker) -> None:
        self._config = config
        self._daily_tracker = daily_tracker

    @classmethod
    def create(cls) -> Session:
        """
        Instantiate a new session.
        """
        config = Config.load()
        cls._database.connect(config["core.database"])

        date = datetime.datetime.now()
        daily_tracker = DailyTracker.from_date(date)

        return Session(config=config, daily_tracker=daily_tracker)

    @property
    def config(self) -> Config:
        return self._config

    @property
    def date(self) -> datetime.date:
        """Return the current date of the working day."""
        return self._daily_tracker.date

    @property
    def daily_tracker(self) -> DailyTracker:
        return self._daily_tracker

    def bind_context(self, ctx: click.Context) -> None:
        """
        Register the current session into Click context.
        """
        ctx.obj = self
        ctx.call_on_close(self.teardown)

    def teardown(self) -> None:
        """
        Close the database connexion at Click teardown.
        """
        self._database.close()


def get_current_session() -> Session:
    """
    Get the current session from the Click context.
    """
    ctx = click.get_current_context()
    if not isinstance(ctx.obj, Session):
        raise SessionError(
            "It appears that you are trying to invoke a command outside "
            "of the CLI context"
        )

    return ctx.obj
