import functools
from datetime import datetime
from enum import Enum, auto
from typing import Callable, List

from peewee import (
    AutoField,
    TextField,
    IntegerField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    Model,
    OperationalError,
)

from hyperfocus.database import database
from hyperfocus.exceptions import DatabaseError, DatabaseNotinitializedError


def db_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as error:
            if "no such table" in str(error):
                raise DatabaseNotinitializedError()
            raise DatabaseError()

    return wrapper


def wrap_methods(decorator: Callable, methods: List[str]):
    def wrapper(cls):
        for method in methods:
            setattr(cls, method, decorator(getattr(cls, method)))
        return cls

    return wrapper


class BaseModel(Model):
    class Meta:
        database = database()


class Status(Enum):
    TODO = auto()
    BLOCKED = auto()
    DELETED = auto()
    DONE = auto()


@wrap_methods(db_error_handler, ["save", "get_or_create"])
class DailyTracker(BaseModel):
    date = DateField(primary_key=True, default=datetime.now().date())
    task_increment = IntegerField(default=0)

    @property
    def next_task_id(self):
        return self.task_increment + 1


@wrap_methods(db_error_handler, ["save"])
class Task(BaseModel):
    _id = AutoField()
    id = IntegerField()
    title = TextField()
    details = TextField(null=True)
    status = IntegerField(default=Status.TODO.value)
    postponed_at = DateField(null=True)
    updated_at = DateTimeField(default=datetime.now())
    daily_tracker = ForeignKeyField(DailyTracker, backref="tasks", null=True)

    class Meta:
        table_name = "tasks"
        indexes = ((("id", "daily_tracker"), True),)


MODELS = [DailyTracker, Task]
