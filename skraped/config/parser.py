import os
import logging
import argparse
import yaml
from yaml import load, dump

lgr = logging.getLogger()


SETTINGS_PATH = './settings.yaml'

CONFIG_MAPPING = {
    'o': 'output_path',
    'kw': 'keywords',
    'sources': 'sources'
}


def parse_cli_args():
    """Parses arguments passed through cli"""
    parser = argparse.ArgumentParser(
        description='Welcome to Skraper, a job scrapper and aggregator CLI tool to help you through your job search.',
        epilog='Goodluck in your job hunt !!'
    )
    parser.add_argument(
        '--o', '-o', type=str, dest='output_path', action='store', required=False,
        help='The directory where the search results will be saved in')

    parser.add_argument(
        '--kw', '-kw', type=str, dest='keywords', action='store', required=False,
        help='The keyword(s) to perform job search on')

    parser.add_argument(
        '--sources',  dest='sources', nargs='*', required=False, help='The sources of the jobs to be scraped. Currently supports BrighterMonday and Glassdoor')

    return parser.parse_args()


def parse_yaml_args():
    """Parses config from settings.yml"""
    settings_file_exists = os.path.exists(SETTINGS_PATH)
    if settings_file_exists:
        with open(SETTINGS_PATH, 'r') as yaml_conf:
            settings = load(yaml_conf, Loader=yaml.FullLoader)
        return settings if settings else {}
    else:
        lgr.error(
            'Missing settings.yaml file. Add settings.yaml to the root directory of the project')
    return {}


def parse_config():
    """Parses all config args, prioritizing cli args over those declared in settings.yml"""
    cli_config = parse_cli_args()
    yaml_config = parse_yaml_args()
    config = yaml_config if yaml_config != {} else cli_config
    for k, v in cli_config.__dict__.items():
        if v is not None:
            config[k] = v
    return config
