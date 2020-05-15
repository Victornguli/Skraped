"""
Common validator utility functions
"""
import logging
import validators
from urllib.parse import urlparse


lgr = logging.getLogger(__name__)


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
