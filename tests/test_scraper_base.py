import pytest
from skraped.scraper_base import ScraperBase


def test_get_class_instance():
    config = {}
    class_instance = ScraperBase.get_class_instance(
        'ScraperBase', config=config)
    assert hasattr(class_instance, '__class__')
    print(class_instance)

