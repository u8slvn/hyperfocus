from __future__ import annotations

import re

from typing import Any
from typing import Callable
from typing import Type
from typing import TypeVar


T = TypeVar("T")

url_regex = re.compile(
    (
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$"
    ),
    re.IGNORECASE,
)


def wrap_methods(
    decorator: Callable[[Type[T]], Any], methods: list[str]
) -> Callable[[Type[T]], Any]:
    """
    Wraps all methods of a class with the given decorator.
    """

    def wrapper(cls: Type[T]) -> Any:
        for method in methods:
            setattr(cls, method, decorator(getattr(cls, method)))
        return cls

    return wrapper


def is_valid_url(url: str) -> bool:
    """
    Check if the given URL is valid.
    """
    return re.match(url_regex, url) is not None
