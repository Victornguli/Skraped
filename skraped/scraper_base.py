import logging
import requests
from bs4 import BeautifulSoup

lgr = logging.getLogger(__name__)

# TODO: Add a base requests method/config to be used by each scraper class


class ScraperBase():
    """Base class implementing core scraping functionality"""

    def __init__(self, config={}):
        self.config = config

    def scrape(self):
        """Entry Point to the execution of all scrape scources defined in the config"""
        scraper_classes = self.config.sources
        for scraper_class in scraper_classes:
            class_instance = self.get_class_instance(
                scraper_class, config=self.config)
            self.call_class_method(
                class_instance, 'scrape', config=self.config)

    def get_next_page(self, *args, **kwargs):
        raise NotImplementedError

    def extract_jobs_from_page(self, *args, **kwargs):
        raise NotImplementedError

    def extract_jobs_from_details(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def call_class_method(class_instance, function_name, **kwargs):
        """Calls calls a function from the passed in class instance"""
        try:
            if class_instance is not None and function_name:
                return getattr(class_instance, function_name)(**kwargs)
        except AttributeError:
            lgr.warning(
                f'method {function_name} does not exist in {class_instance}')
        return None

    @staticmethod
    def get_class_instance(class_name, **kwargs):
        """Retrieves a class instance to be used for running individual scrapers"""
        if class_name in globals() and hasattr(globals()[class_name], '__class__'):
            try:
                return globals()[class_name](**kwargs)
            except TypeError:
                lgr.warning(f'{class_name} cannot be retrieved.')
        return None
