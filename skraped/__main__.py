import sys
import logging
from skraped.config.parser import parse_config
from skraped.config.validate_config import validate_conf
from skraped.config.log_conf import configure_logging
from skraped.scraper_base import ScraperBase

configure_logging()
lgr = logging.getLogger('main')


def main():
    config = parse_config()
    pass


def get_class_instance(class_name, **kwargs):
    """Retrieves a class instance to be used for running individual scrapers"""
    if class_name in globals() and hasattr(globals()[class_name], '__class__'):
        try:
            return globals()[class_name](**kwargs)
        except TypeError:
            lgr.warning(f'{class_name} cannot be retrieved.')
    return None


def call_class_method(class_instance, function_name, **kwargs):
    """
        Calls calls a function from the passed in class instance
    """
    try:
        if class_instance is not None and function_name:
            return getattr(class_instance, function_name)(**kwargs)
    except AttributeError:
        lgr.warning(
            f'method {function_name} does not exist in {class_instance}')
    return None


if __name__ == "__main__":
    main()
