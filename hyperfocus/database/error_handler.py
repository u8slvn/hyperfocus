from __future__ import annotations

import functools

import peewee

from hyperfocus.database.exceptions import DatabaseError


def db_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except peewee.DatabaseError as error:
            if "no such table" in str(error):
                raise DatabaseError(
                    "Database not initialized, please run init command first"
                )
            raise DatabaseError(f"Unexpected database error: {error}")

    return wrapper
