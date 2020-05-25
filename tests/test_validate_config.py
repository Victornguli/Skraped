import argparse
import pytest
from unittest import TestCase
from skraped.config.validate_config import validate_conf, ConfigError, validate_output_path, validate_sources


class TestValidateConfig(TestCase):
    def setUp(self):
        self.valid_config = {
            'output_path': 'data', 'sources': ['Glassdoor', 'BrighterMonday'],
            'keywords': 'Software Developer'}
        self.invalid_config = {
            'output_path': 'data', 'sources': ['Glassdoor', 'BrighterMonday', 'RandomJobSite'],
            'keywords': 'Software Developer'}

    def test_validate_config(self):
        """Tests for config validation method"""
        with pytest.raises(ConfigError):
            validate_conf(self.invalid_config)

    def test_validate_path_fail(self):
        with pytest.raises(ConfigError):
            validate_output_path('', self.valid_config)

    def test_validate_sources_fail(self):
        with pytest.raises(ConfigError):
            validate_sources(['Linkedin', 'RandomJobSite'], self.valid_config)
