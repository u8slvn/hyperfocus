from datetime import datetime

from hyperfocus.config import Config
from hyperfocus.database import database
from hyperfocus.services import DailyTrackerService


class Session:
    def __init__(self):
        config = Config.load()
        database.connect(db_path=config.db_path)
        now = datetime.now().date()
        self.daily_tracker: DailyTrackerService = DailyTrackerService(date=now)

    def is_a_new_day(self) -> bool:
        return self.daily_tracker.new_day

    @property
    def date(self):
        return self.daily_tracker.date
