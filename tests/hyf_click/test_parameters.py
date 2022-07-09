import re

import click
from click.testing import CliRunner

from hyperfocus.hyf_click.parameters import NotRequired, NotRequiredIf
from tests.conftest import pytest_regex


runner = CliRunner()


def test_click_option_not_required_params():
    @click.command()
    @click.option("--hello", is_flag=True, cls=NotRequired, not_required=["bye"])
    @click.option("--bye", is_flag=True, cls=NotRequired, not_required=["hello"])
    def foo(hello, bye):
        click.echo("bar")

    try1 = runner.invoke(foo, ["--hello", "--bye"])
    try2 = runner.invoke(foo, ["--hello"])
    try3 = runner.invoke(foo, ["--bye"])

    expected = pytest_regex(
        r"^(.*)Unnecessary option 'bye' provided(.*)$",
        flags=re.MULTILINE,
    )
    assert expected == try1.stdout
    assert try2.output == "bar\n"
    assert try3.output == "bar\n"


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
