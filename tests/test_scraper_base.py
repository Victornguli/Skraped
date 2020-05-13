import pytest
from skraped.scraper_base import ScraperBase


def test_get_class_instance():
    config = {}
    class_instance = ScraperBase.get_class_instance(
        'ScraperBase', config=config)
    assert hasattr(class_instance, '__class__')


def test_call_class_method():
    class_instance = ScraperBase.get_class_instance(
        class_name='ScraperBase')
    assert ScraperBase.call_class_method(
        class_instance, 'missing_fn') is None
    assert ScraperBase.call_class_method(
        class_instance, 'get_class_instance', class_name='ScraperBase') is not None
