from __future__ import annotations

from datetime import datetime
from enum import IntEnum, auto

import peewee

from hyperfocus.database import database
from hyperfocus.database.error_handler import db_error_handler
from hyperfocus.utils import wrap_methods


class TaskStatus(IntEnum):
    TODO = auto()
    BLOCKED = auto()
    DELETED = auto()
    DONE = auto()


class BaseModel(peewee.Model):
    class Meta:
        database = database()


@wrap_methods(db_error_handler, ["save", "get_or_create"])
class DailyTracker(BaseModel):
    date = peewee.DateField(primary_key=True, default=datetime.now().date())
    task_increment = peewee.IntegerField(default=0)

    @property
    def next_task_id(self):
        return self.task_increment + 1


@wrap_methods(db_error_handler, ["save", "get_or_none"])
class Task(BaseModel):
    _id = peewee.AutoField()
    id = peewee.IntegerField()
    title = peewee.TextField()
    details = peewee.TextField(null=True)
    status = peewee.IntegerField(default=TaskStatus.TODO)
    postponed_at = peewee.DateField(null=True)
    updated_at = peewee.DateTimeField(default=datetime.now())
    daily_tracker = peewee.ForeignKeyField(DailyTracker, backref="tasks", null=True)

    class Meta:
        table_name = "tasks"
        indexes = ((("id", "daily_tracker"), True),)


MODELS = [DailyTracker, Task]
