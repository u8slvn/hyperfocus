from __future__ import annotations

import re

import click

from click.testing import CliRunner

from hyperfocus.console.core.parameters import NotRequired
from hyperfocus.console.core.parameters import NotRequiredIf
from tests.conftest import pytest_regex


runner = CliRunner()


def test_click_option_not_required_params():
    @click.command()
    @click.option("--foo", is_flag=True, cls=NotRequired, not_required=["bar"])
    @click.option("--bar", is_flag=True, cls=NotRequired, not_required=["foo"])
    def dummy(foo, bar):
        click.echo("test")

    try1 = runner.invoke(dummy, ["--foo", "--bar"])
    try2 = runner.invoke(dummy, ["--foo"])
    try3 = runner.invoke(dummy, ["--bar"])

    expected = pytest_regex(
        r"^(.*)Unnecessary option 'bar' provided(.*)$",
        flags=re.MULTILINE,
    )
    assert expected == try1.stdout
    assert try2.output == "test\n"
    assert try3.output == "test\n"


def test_click_argument_not_required_if_param():
    @click.command()
    @click.option("--opt1", is_flag=True)
    @click.option("--opt2", is_flag=True)
    @click.argument("name", cls=NotRequiredIf, not_required_if=["opt2"])
    def foo(name: str, opt1: bool, opt2: bool):
        click.echo("bar")

    try1 = runner.invoke(foo, ["--opt1"])
    try2 = runner.invoke(foo, ["--opt2"])

    expected = pytest_regex(
        r"^(.*)Missing argument 'NAME'(.*)$",
        flags=re.MULTILINE,
    )
    assert try1.output == expected
    assert try2.output == "bar\n"
