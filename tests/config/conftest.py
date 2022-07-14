from pathlib import Path

import pytest


@pytest.fixture
def dummy_dir():
    return Path("/dummy")
