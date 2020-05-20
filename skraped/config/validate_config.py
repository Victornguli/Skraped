import os
import logging

lgr = logging.getLogger()


VALID_CONFIG = {
    'output_path': './',
    'sources': ['Linkedin', 'BrighterMonday', 'Glassdoor'],
    'keywords': 'Python Developer'
}


class ConfigError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'ConfigError: {self.message} config is invalid'
        else:
            return f'ConfigError: the configuration passed is invalid'


def validate_sources(sources):
    """Validates the sources"""
    if not isinstance(sources, list) or not sources:
        raise ConfigError('sources')
    for source in sources:
        if source not in VALID_CONFIG['sources']:
            raise ConfigError('sources')


def validate_output_path(path):
    """Validates the output path defined"""
    if not path or not isinstance(path, str):
        raise ConfigError('path')
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path):
        raise ConfigError('path')


def validate_conf(conf):
    """Validates a config before running the scraper"""
    for conf_item in conf:
        if conf_item not in VALID_CONFIG:
            raise ConfigError(conf_item)
    validate_sources(conf.get('sources', []))
    validate_output_path(conf.get('output_path', ''))


if __name__ == '__main__':
    validate_output_path('./data')
