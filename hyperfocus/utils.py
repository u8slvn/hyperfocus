from __future__ import annotations

from typing import Any, Callable


def wrap_methods(decorator: Callable, methods: list[str]) -> Callable:
    """
    Wraps all methods of a class with the given decorator.
    """

    def wrapper(cls) -> Any:
        for method in methods:
            setattr(cls, method, decorator(getattr(cls, method)))
        return cls

    return wrapper
