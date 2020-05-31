import os
import logging
import argparse
import yaml
from yaml import load, dump

lgr = logging.getLogger()

base_path = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SETTINGS_PATH = os.path.normpath(os.path.join(base_path, 'settings.yaml'))


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
        '--kw', '-kw', nargs='*', dest='keywords', action='store', required=False,
        help='The keyword(s) to perform job search on')

    parser.add_argument(
        '-s', '-settings', type=str, dest='settings', action='store', required=False,
        help='The full path to settings.yaml file for custom configuration'
    )
    return parser.parse_args()


def parse_yaml_args(settings_path=''):
    """Parses config from settings.yml"""
    settings_path = os.path.abspath(
        settings_path) if settings_path else DEFAULT_SETTINGS_PATH
    settings_file_exists = os.path.exists(settings_path)
    if settings_file_exists:
        with open(settings_path, 'r') as yaml_conf:
            settings = load(yaml_conf, Loader=yaml.FullLoader)
        return settings if settings else {}
    else:
        lgr.error(
            'Missing settings.yaml file. Add settings.yaml to the root directory of the project')
    raise FileNotFoundError(f"Settings file {settings_path} does not exist")


def parse_config():
    """Parses all config args, prioritizing cli args over those declared in settings.yml"""
    cli_config = parse_cli_args()
    yaml_config = parse_yaml_args(settings_path=cli_config.settings)
    # @TODO: Better config precedence
    config = yaml_config
    for k, v in cli_config.__dict__.items():
        if v is not None:
            config[k] = v
    config["keywords"] = "".join(config["keywords"])
    return config
