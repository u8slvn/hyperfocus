from datetime import datetime

import click

from hyperfocus.config import Config
from hyperfocus.database import database
from hyperfocus.services import DailyTrackerService


class Session:
    def __init__(self, ctx: click.Context):
        config = Config.load()
        database.connect(db_path=config.db_path)
        now = datetime.now().date()
        self.daily_tracker: DailyTrackerService = DailyTrackerService(date=now)

        ctx.obj = self

    def is_a_new_day(self) -> bool:
        return self.daily_tracker.new_day

    @property
    def date(self):
        return self.daily_tracker.date


def get_current_session() -> Session:
    ctx = click.get_current_context()
    if not isinstance(ctx.obj, Session):
        raise Exception()  # TODO: add typed exception

    return ctx.obj
