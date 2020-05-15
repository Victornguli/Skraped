"""
Common validator utility functions
"""
import logging
import validators
from urllib.parse import urlparse
from skraped.config.log_conf import configure_logging
# from skraped.scraper_base import ScraperBase

configure_logging()

lgr = logging.getLogger('main')


def validate_and_parse_url(url):
    """
    Validates and parse a url string to return appropriate url parts e.g scheme, base url, etc
    :param url: The url string to be validated and parsed
    :type url: str
    :return: str | None
    """
    url = str(url)
    if validators.url(url):
        parsed_url = urlparse(url)
        return {
            'scheme': parsed_url.scheme, 'base': parsed_url.netloc, 'path': parsed_url.path, 'params':
            parsed_url.params, 'query': parsed_url.query}
    return None
