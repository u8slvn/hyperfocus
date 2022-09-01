from __future__ import annotations

import datetime
import uuid
from enum import IntEnum, auto

import peewee

from hyperfocus.database import database
from hyperfocus.database.error_handler import db_error_handler
from hyperfocus.utils import wrap_methods


class TaskStatus(IntEnum):
    TODO = auto()
    STASHED = auto()
    DELETED = auto()
    DONE = auto()


class BaseModel(peewee.Model):
    class Meta:
        database = database()


@wrap_methods(db_error_handler, ["save", "get_or_create", "get_or_none"])
class WorkingDay(BaseModel):
    date = peewee.DateField(primary_key=True)
    task_increment = peewee.IntegerField(default=0)
    locked = peewee.BooleanField(default=False)

    @property
    def next_task_id(self):
        self.task_increment += 1
        return self.task_increment


@wrap_methods(db_error_handler, ["save", "get_or_none"])
class Task(BaseModel):
    uuid = peewee.UUIDField(primary_key=True, default=uuid.uuid4)
    id = peewee.IntegerField()
    title = peewee.TextField()
    details = peewee.TextField(null=True)
    status = peewee.IntegerField(default=TaskStatus.TODO)
    parent_task = peewee.ForeignKeyField("self", null=True)
    working_day = peewee.ForeignKeyField(WorkingDay, backref="tasks", null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "tasks"
        indexes = ((("uuid", "working_day"), True),)

    def save(self, *args, **kwargs) -> Task:
        # Auto update 'updated_at' field at each save.
        self.updated_at = datetime.datetime.now()
        return super(Task, self).save(*args, **kwargs)


MODELS = [WorkingDay, Task]
