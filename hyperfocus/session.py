from datetime import datetime

import click

from hyperfocus.config import Config
from hyperfocus.database import database
from hyperfocus.exceptions import SessionError
from hyperfocus.services import DailyTrackerService


class Session:
    def __init__(self):
        config = Config.load()
        database.connect(db_path=config.db_path)
        now = datetime.now().date()
        self.daily_tracker: DailyTrackerService = DailyTrackerService(date=now)

    def bind_context(self, ctx: click.Context):
        ctx.obj = self

    def is_a_new_day(self) -> bool:
        return self.daily_tracker.new_day

    @property
    def date(self):
        return self.daily_tracker.date


def get_current_session() -> Session:
    ctx = click.get_current_context()
    if not isinstance(ctx.obj, Session):
        raise SessionError(
            "It appears that you are trying to invoke a command outside "
            "of the CLI context"
        )

    return ctx.obj
