import pytest

from hyperfocus.termui import printer
from hyperfocus.termui.components import SuccessNotification


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ("[red bold]foo[/]bar", "foobar\n"),
        (SuccessNotification("foobar"), "✔(success) foobar\n"),
    ],
)
def test_echo(capsys, inputs, expected):
    printer.echo(inputs)

    captured = capsys.readouterr()
    assert captured.out == expected


def test_pager_echo(capsys):
    def text():
        for line in ["foo", "bar", "baz"]:
            yield f"{line}\n"

    printer.pager_echo(text())

    captured = capsys.readouterr()
    assert captured.out == ("foo\n" "bar\n" "baz\n" "\n")


def test_banner(capsys):
    printer.banner("foobar")

    captured = capsys.readouterr()
    assert captured.out == "> foobar\n"


def test_config(capsys):
    config = {
        "core.database": "/database.sqlite",
        "alias.st": "status",
    }

    printer.config(config)

    expected = "core.database = /database.sqlite\n" "alias.st = status\n"
    captured = capsys.readouterr()
    assert captured.out == expected
