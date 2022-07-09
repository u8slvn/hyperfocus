from __future__ import annotations

import re
from typing import Callable, List


def wrap_methods(decorator: Callable, methods: List[str]):
    def wrapper(cls):
        for method in methods:
            setattr(cls, method, decorator(getattr(cls, method)))
        return cls

    return wrapper


def un_camel_case(camel_case_str: str):
    return re.sub(r"([A-Z])", r" \1", camel_case_str).lower().strip()
