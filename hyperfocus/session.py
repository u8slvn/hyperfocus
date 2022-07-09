from __future__ import annotations

from typing import TYPE_CHECKING

import click

from hyperfocus.config.config import Config
from hyperfocus.database import database
from hyperfocus.exceptions import SessionError
from hyperfocus.services import DailyTrackerService, PastTrackerService


if TYPE_CHECKING:
    import datetime


class Session:
    _database = database

    def __init__(self) -> None:
        self.config = Config.load()
        self._database.connect(self.config["core.database"])
        self.daily_tracker: DailyTrackerService = DailyTrackerService.today()
        self.past_tracker: PastTrackerService = PastTrackerService(
            current_day=self.daily_tracker
        )

    @property
    def date(self) -> datetime.date:
        return self.daily_tracker.date

    def is_a_new_day(self) -> bool:
        return self.daily_tracker.new_day

    def bind_context(self, ctx: click.Context) -> None:
        ctx.obj = self
        ctx.call_on_close(self.teardown)

    def teardown(self) -> None:
        self._database.close()


def get_current_session() -> Session:
    ctx = click.get_current_context()
    if not isinstance(ctx.obj, Session):
        raise SessionError(
            "It appears that you are trying to invoke a command outside "
            "of the CLI context"
        )

    return ctx.obj
