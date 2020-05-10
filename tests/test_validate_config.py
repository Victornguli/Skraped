import argparse
import pytest
from config.validate_config import validate_conf, ConfigError, validate_output_path, validate_sources


def test_validate_config():
    """Tests for config validation method"""
    conf = {
        'output_path': '', 'sources': ['Linkedin', 'BrighterMonday', 'MyJobMag'],
        'keywords': 'Software Developer'}
    with pytest.raises(ConfigError):
        validate_conf(conf)


def test_validate_path_fail():
    with pytest.raises(ConfigError):
        validate_output_path('')


def test_validate_sources_fail():
    with pytest.raises(ConfigError):
        validate_sources(['Linkedin', 'RandomJobSite'])
