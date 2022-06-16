import re
from pathlib import Path

import pytest

TEST_DIR = Path(__file__).parent.resolve()
FIXTURES_DIR = TEST_DIR / "fixtures"


@pytest.fixture()
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture(scope="session")
def tmp_test_dir(tmpdir_factory):
    return Path(tmpdir_factory.mktemp("hyperfocus"))


@pytest.fixture
def cli_config(mocker, tmp_test_dir):
    file_path = tmp_test_dir / "config.ini"

    mocker.patch("hyperfocus.config.DIR_PATH", tmp_test_dir)
    mocker.patch("hyperfocus.config.FILE_PATH", file_path)


class pytest_regex:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return self._regex.pattern
