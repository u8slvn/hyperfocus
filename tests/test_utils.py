from __future__ import annotations

import pytest

from hyperfocus.utils import is_valid_url


@pytest.mark.parametrize(
    "url, expected",
    [
        ("http://example.com", True),
        ("https://example.com", True),
        ("https://example.com/path", True),
        ("https://example.com/path?query=value", True),
        ("ftp://example.com", True),
        ("http://localhost:8000", True),
        ("https://sub.domain.example.com", True),
        ("htp://example.com", False),
        ("http:/example.com", False),
        ("http://", False),
        ("http://example", False),
        ("example.com", False),
        ("http://-example.com", False),
        ("http://.example.com", False),
        ("http://example..com", False),
        ("http://example.com:abc", False),
    ],
)
def test_is_valid_url(url, expected):
    assert is_valid_url(url) == expected
