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
            error_message = f"Unexpected database error: {error}"
            if "no such table" in str(error):
                error_message = (
                    "Database not initialized, please run init command first"
                )
            raise DatabaseError(error_message) from error

    return wrapper
