from __future__ import annotations

import pytest

from hyperfocus.termui.exceptions import TermUIError
from hyperfocus.termui.markup import markup


@pytest.mark.parametrize(
    "markup_text, expected",
    [
        ("[red]foo[/]", "\x1b[31mfoo\x1b[0m"),
        ("[red]foo[/] [blue]bar[/]", "\x1b[31mfoo\x1b[0m \x1b[34mbar\x1b[0m"),
        (
            "[link=https://example.com]example[/]",
            "\033]8;;https://example.com\007example\033]8;;\007",
        ),
        (
            "[red]Check this [link=https://example.com]link[/] out[/]",
            "\x1b[31mCheck this \033]8;;https://example.com\007link\033]8;;\007 out\x1b[0m",
        ),
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
        ("[link=https://example.com]example[/]", "example"),
        (
            "[red]Check this [link=https://example.com]link[/] out[/]",
            "Check this link out",
        ),
    ],
)
def test_remove_markup(markup_text, expected):
    output = markup.remove(markup_text)

    assert output == expected


def test_markup_error():
    with pytest.raises(TermUIError):
        markup.resolve("[foo]bar[/]")
