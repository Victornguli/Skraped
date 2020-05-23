import os
import sys
import logging
import csv
from skraped.config.parser import parse_config
from skraped.config.validate_config import validate_conf
from skraped.scraper_base import ScraperBase
from skraped.glassdoor import Glassdoor
from skraped.brighter_monday import BrighterMonday


lgr = logging.getLogger()
lgr.setLevel('INFO')
logging.basicConfig(filename='basic.log', level='INFO')

if lgr.level == 20:
    lgr.addHandler(logging.StreamHandler(sys.stdout))
else:
    lgr.addHandler(logging.StreamHandler())


def main():
    config = parse_config()
    validate_conf(config)
    base = ScraperBase(config)
    scraper_classes = config.get('sources')
    # return config
    for scraper in scraper_classes:
        class_instance = get_class_instance(scraper, config=config)
        if class_instance is None:
            lgr.error(
                f'Failed to retrieve the Scraper Class {scraper}. Exiting...')
            sys.exit()
        res = get_class_method(class_instance, 'scrape')()
        base.save_to_csv(res)


def get_class_instance(class_name, **kwargs):
    """Retrieves a class instance to be used for running individual scrapers"""
    if class_name in globals() and hasattr(globals()[class_name], '__class__'):
        try:
            return globals()[class_name](**kwargs)
        except TypeError:
            lgr.warning(f'{class_name} cannot be retrieved.')
    return None


def get_class_method(class_instance, function_name, **kwargs):
    """
    Retrives a class function from the passed in class instance
    """
    try:
        if class_instance is not None and function_name:
            return getattr(class_instance, function_name)
    except AttributeError:
        lgr.warning(
            f'method {function_name} does not exist in {class_instance}')
    return None


if __name__ == "__main__":
    main()
