import os
import logging

lgr = logging.getLogger()


VALID_CONFIG = {
    'output_path': (str, ''),
    'log_path': (str, ''),
    'sources': (list, ['Linkedin', 'BrighterMonday', 'Glassdoor']),
    'keywords': (str, ''),
    'settings': (str, ''),
    'delay': (int, 0)
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


def validate_sources(sources, conf):
    """Validates the sources"""
    if not isinstance(sources, VALID_CONFIG['sources'][0]) or not sources:
        raise ConfigError('sources')
    for source in sources:
        if source not in VALID_CONFIG['sources'][1]:
            raise ConfigError('sources')


def validate_output_path(path, config):
    """Validates the output path defined"""
    if not path or not isinstance(path, VALID_CONFIG['output_path'][0]):
        raise ConfigError('path')
    output_path = path
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path):
        raise ConfigError('path')
    normalized_path = os.path.abspath(output_path)
    config['output_path'] = normalized_path


def validate_conf(conf):
    """Validates a config before running the scraper"""
    for conf_item in conf:
        if conf_item not in VALID_CONFIG:
            raise ConfigError(conf_item)
    validate_sources(conf.get('sources', []), conf)
    validate_output_path(conf.get('output_path', ''), conf)
