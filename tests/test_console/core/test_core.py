from click.testing import CliRunner


runner = CliRunner()


def test_hyperfocus_command_return_command_without_checking_for_alias(hyf_group):
    result = runner.invoke(hyf_group, ["alias"])

    assert result.output == "alias\n"


def test_hyperfocus_command_handle_alias(mocker, hyf_group):
    config = {"alias.sailas": "alias"}
    mocker.patch("hyperfocus.console.core.group.Config.load", return_value=config)

    result = runner.invoke(hyf_group, ["sailas"])

    assert result.output == "alias\n"
