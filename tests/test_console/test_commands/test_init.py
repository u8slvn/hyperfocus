from __future__ import annotations

import pytest

from click.testing import CliRunner

from hyperfocus.config.config import Config
from tests.conftest import pytest_regex


runner = CliRunner()


@pytest.mark.functional
def test_init(monkeypatch, base_cli, test_dir):
    monkeypatch.setattr(Config, "_dir", test_dir)
    config_path = test_dir / Config._filename
    db_path = test_dir / "test_init_db_.sqlite"

    result = runner.invoke(base_cli, ["init"], input=f"{db_path}\n")

    expected = pytest_regex(
        r"\? Database location \[(.*)\]: (.*)test_init_db_.sqlite\n"
        r"ℹ\(info\) Config file created successfully in (.*)config.ini\n"  # noqa: RUF001
        r"ℹ\(info\) Database initialized successfully in (.*)test_init_db_.sqlite\n"  # noqa: RUF001
    )
    assert result.exit_code == 0
    assert expected == result.output
    assert db_path.exists()
    assert config_path.exists()
