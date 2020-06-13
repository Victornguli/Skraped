import os
import sys
import logging
import csv
import time
from datetime import datetime
from skraped.config.parser import parse_config
from skraped.config.validate_config import validate_conf
from skraped.scraper_base import ScraperBase
from skraped.glassdoor import Glassdoor
from skraped.brighter_monday import BrighterMonday


t_start = time.perf_counter()

lgr = logging.getLogger()
lgr.setLevel('INFO')
logging.basicConfig(filename='logs.log', level='INFO')

if lgr.level == 20:
    lgr.addHandler(logging.StreamHandler(sys.stdout))
else:
    lgr.addHandler(logging.StreamHandler())


def main():  # pragma: nocover
    lgr.info("Initialized Skraper at {}".format(datetime.now().strftime("%d/%m/%y %H:%M %p")))
    config = parse_config(sys.argv[1:])
    return config
    validate_conf(config)
    base = ScraperBase(config)
    if config["recover"]:
        base.recover_scraped_data()
        return
    scraper_classes = config.get('sources')
    scrape_data = []
    for scraper in scraper_classes:
        class_instance = get_class_instance(scraper, config=config)
        if class_instance is None:
            lgr.error(
                f'Failed to retrieve the Scraper Class {scraper}. Exiting...')
            sys.exit()
        scrape_data.extend(get_class_method(class_instance, 'scrape')())

    scrape_data = base.merge_scrape_data(scrape_data)
    base.save_pickle(scrape_data)
    base.save_csv(scrape_data)

    t_end = time.perf_counter()
    lgr.info("Complete!! Skraper ran for {} second(s)".format(round(t_end - t_start, 2)))
    return


def get_class_instance(class_name, **kwargs):
    """Retrieves a class instance to be used for running individual scrapers"""
    if class_name in globals() and hasattr(globals()[class_name], '__class__'):
        try:
            return globals()[class_name](**kwargs)
        except TypeError:  # pragma: nocover
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
