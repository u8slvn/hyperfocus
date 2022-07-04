import functools
from datetime import datetime
from enum import Enum, IntEnum, auto
from typing import Callable, List

from peewee import (
    AutoField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    OperationalError,
    TextField,
)

from hyperfocus.database import database
from hyperfocus.exceptions import DatabaseError


def wrap_methods(decorator: Callable, methods: List[str]):
    def wrapper(cls):
        for method in methods:
            setattr(cls, method, decorator(getattr(cls, method)))
        return cls

    return wrapper


def db_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as error:
            if "no such table" in str(error):
                raise DatabaseError(
                    "Database not initialized, please run init command first"
                )
            raise DatabaseError("Unexpected database error")

    return wrapper


class TaskEvents(str, Enum):
    INIT = "init"
    NO_CHANGE = "no change"
    UPDATED = "updated"
    NOT_FOUND = "not found"
    CREATED = "created"


class TaskStatus(IntEnum):
    TODO = auto()
    BLOCKED = auto()
    DELETED = auto()
    DONE = auto()


class BaseModel(Model):
    class Meta:
        database = database()


@wrap_methods(db_error_handler, ["save", "get_or_create"])
class DailyTracker(BaseModel):
    date = DateField(primary_key=True, default=datetime.now().date())
    task_increment = IntegerField(default=0)

    @property
    def next_task_id(self):
        return self.task_increment + 1


@wrap_methods(db_error_handler, ["save", "get_or_none"])
class Task(BaseModel):
    _id = AutoField()
    id = IntegerField()
    title = TextField()
    details = TextField(null=True)
    status = IntegerField(default=TaskStatus.TODO)
    postponed_at = DateField(null=True)
    updated_at = DateTimeField(default=datetime.now())
    daily_tracker = ForeignKeyField(DailyTracker, backref="tasks", null=True)

    class Meta:
        table_name = "tasks"
        indexes = ((("id", "daily_tracker"), True),)


MODELS = [DailyTracker, Task]
