from click.testing import CliRunner

from hyperfocus import __app_name__, __version__
from hyperfocus.console.cli import hyf


runner = CliRunner()


def test_main_cmd_version():
    result = runner.invoke(hyf, ["--version"])

    expected = f"{__app_name__}, version {__version__}\n"
    assert expected == result.stdout
