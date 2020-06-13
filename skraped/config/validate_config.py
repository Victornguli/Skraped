import os
import logging
from ..utils import parse_pickle_name

lgr = logging.getLogger()


VALID_CONFIG = {
    'output_path': (str, ''),
    'log_path': (str, ''),
    'sources': (list, ['Linkedin', 'BrighterMonday', 'Glassdoor']),
    'keywords': (str, ''),
    'settings': (str, ''),
    'delay': (bool, False),
    'delay_range': (dict, {'min_delay': (int, 0), 'max_delay': (int, 0)}),
    'pickle_path': (str, ''),
    'recover': (bool, '')
}

# @TODO: Add recurvise validation for nested configuration items

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


def validate_pickle_date(pickle_date, conf):
    """Validates the pickle date passed, if any, and sets-up the recovery flag in conf"""
    pickle_name = parse_pickle_name(pickle_date)
    if pickle_date:
        conf["recover"] = True
    else:
        conf["recover"] = False
    
    pickle_dir = os.path.join(conf["output_path"], "pickles")
    if not os.path.exists(pickle_dir):
        os.mkdir(pickle_dir)
    conf["pickle_path"] = os.path.join(pickle_dir, pickle_name)
    

def validate_conf(conf):
    """Validates a config before running the scraper"""
    for conf_item in conf:
        if conf_item not in VALID_CONFIG:
            raise ConfigError(conf_item)
    validate_sources(conf.get('sources', []), conf)
    validate_output_path(conf.get('output_path', ''), conf)
    validate_pickle_date(conf.get('pickle_path', ''), conf)
