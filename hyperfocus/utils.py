from typing import Callable, List


def wrap_methods(decorator: Callable, methods: List[str]):
    def wrapper(cls):
        for method in methods:
            setattr(cls, method, decorator(getattr(cls, method)))
        return cls

    return wrapper
