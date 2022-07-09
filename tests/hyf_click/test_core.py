from tests.hyf_click.test_parameters import runner


def test_hyperfocus_command_handle_alias(mocker, hyf_group):
    config = {"alias.sailas": "alias"}
    mocker.patch("hyperfocus.cli.Config.load", return_value=config)

    result = runner.invoke(hyf_group, ["sailas"])

    assert result.output == "alias\n"
