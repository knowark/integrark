import os
import rapidjson as json
from pytest import raises, fixture
from integrark.core import (
    TrialConfig, DevelopmentConfig, ProductionConfig,
    load_config, build_config)


@fixture
def config_data(tmp_path):
    config_directory = tmp_path / 'configuration'
    config_directory.mkdir()
    config_file = config_directory / "config.json"

    config_dict = {
        'mode': 'PROD',
        'factory': 'WebFactory'
    }

    config_file.write_text(json.dumps(config_dict))

    return config_file, config_dict


def test_trial_config():
    config = TrialConfig()
    assert config['mode'] == 'TEST'


def test_development_config():
    config = DevelopmentConfig()
    assert config['mode'] == 'DEV'


def test_configuration_load_config_no_file():
    path = ''
    result = load_config(path)
    assert result is None


def test_configuration_load_config_with_file(config_data):
    config_file, config_dict = config_data
    config_file.write_text(json.dumps(config_dict))

    result = load_config(str(config_file))
    assert result == config_dict


def test_configuration_build_config_default():
    path = '/tmp/config.json'
    mode = 'DEV'

    config = build_config(path, mode)

    assert isinstance(config, DevelopmentConfig)


def test_configuration_build_config_trial():
    path = '/tmp/config.json'
    mode = 'TEST'

    config = build_config(path, mode)

    assert isinstance(config, TrialConfig)


def test_configuration_build_config_production(config_data):
    config_file, config_dict = config_data
    config_file.write_text(json.dumps(config_dict))
    mode = 'PROD'

    config = build_config(config_file, mode)

    assert isinstance(config, ProductionConfig)


def test_configuration_build_config_none_production_build(config_data):
    config_file, config_dict = config_data
    config_file.write_text(json.dumps(config_dict))
    mode = 'PROD'

    config = build_config("", mode)

    assert isinstance(config, ProductionConfig)