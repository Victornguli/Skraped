import os
import argparse
import pytest
from skraped.config.validate_config import validate_conf, ConfigError, validate_output_path, validate_sources


@pytest.fixture
def invalid_config():
    return {
        'output_path': 'data', 'sources': ['Glassdoor', 'BrighterMonday', 'RandomJobSite'],
        'keywords': 'Software Developer'}


@pytest.fixture
def pre_validation_config(tmpdir):
    return {
        'output_path': str(os.path.join(tmpdir, 'data')), 'sources': ['Glassdoor', 'BrighterMonday'],
        'keywords': 'Software Developer', 'delay': True, 'recover': False,
        'delay_range': {'min_delay': 2, 'max_delay': 10}, 'pickle_path': ''}


def test_validate_config(invalid_config, pre_validation_config):
    """Tests for config validation method"""
    with pytest.raises(ConfigError):
        validate_conf(invalid_config)
    validate_conf(pre_validation_config)


def test_validate_path_fail(valid_config):
    with pytest.raises(ConfigError):
        validate_output_path('', valid_config)


def test_validate_sources_fail(valid_config):
    with pytest.raises(ConfigError):
        validate_sources(['Linkedin', 'RandomJobSite'], valid_config)
