"""
Common utility functions
"""
import os
import logging
import validators
from urllib.parse import urlparse
# from skraped.scraper_base import ScraperBase

lgr = logging.getLogger()


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


# def get_project_root():
#     """
#     Retrieves the full path of the root path for the project
#     """
#     parent_path = os.path.dirname(os.path.dirname(__file__))
#     if os.path.exists(parent_path):
#         print(parent_path)
#         return parent_path
#     return None
