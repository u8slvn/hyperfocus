from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Type
from typing import TypeVar


T = TypeVar("T")


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
