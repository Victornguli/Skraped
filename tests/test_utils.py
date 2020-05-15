import pytest
from skraped.utils import validate_and_parse_url, get_class_instance, call_class_method
from skraped.scraper_base import ScraperBase


def test_validate_and_parse_url():
    """Tests the utility method for validating and parsing a url"""
    url = validate_and_parse_url(
        'https://www.google.com/search?q=How+to+run+python+tests&sourceid=chrome&ie=UTF-8')
    malformed_url = validate_and_parse_url(1)
    assert url.get(
        'base', '') == 'www.google.com', 'url base should be equal to www.google.com'
    assert malformed_url is None, 'Malformed url should return None'


def test_get_class_instance():
    config = {}
    class_instance = get_class_instance(
        'ScraperBase', config=config)
    assert hasattr(class_instance, '__class__')


def test_call_class_method_pass():
    class_instance = get_class_instance(class_name='ScraperBase')
    assert call_class_method(
        class_instance, 'send_request', url='https://www.google.com') is not None


def test_call_class_method_fail():
    class_instance = get_class_instance(
        class_name='ScraperBase')
    assert call_class_method(
        class_instance, 'missing_fn') is None
    assert call_class_method(
        class_instance, 'get_class_instance', class_name='ScraperBase', extra='Non-Existing kw') is None
