from __future__ import annotations

import pytest

from hyperfocus.termui.exceptions import TermUIError
from hyperfocus.termui.markup import markup


@pytest.mark.parametrize(
    "markup_text, expected",
    [
        ("[red]foo[/]", "\x1b[31mfoo\x1b[0m"),
        ("[red]foo[/] [blue]bar[/]", "\x1b[31mfoo\x1b[0m \x1b[34mbar\x1b[0m"),
    ],
)
def test_resolve_markup(markup_text, expected):
    output = markup.resolve(markup_text)

    assert output == expected


@pytest.mark.parametrize(
    "markup_text, expected",
    [
        ("[red]foo[/]", "foo"),
        ("[red]foo[/] [blue]bar[/]", "foo bar"),
    ],
)
def test_remove_markup(markup_text, expected):
    output = markup.remove(markup_text)

    assert output == expected


def test_markup_error():
    with pytest.raises(TermUIError):
        markup.resolve("[foo]bar[/]")
