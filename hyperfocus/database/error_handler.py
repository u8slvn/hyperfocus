from __future__ import annotations

import functools

from typing import Any
from typing import Callable

import peewee

from hyperfocus.database.exceptions import DatabaseError


def db_error_handler(func: Callable[[Any, Any], Any]) -> Callable[[Any, Any], Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except peewee.DatabaseError as error:
            if "no such table" in str(error):
                raise DatabaseError(
                    "Database not initialized, please run init command first"
                )
            raise DatabaseError(f"Unexpected database error: {error}")

    return wrapper
