import pytest
from skraped.__main__ import get_class_instance, call_class_method


def test_get_class_instance():
    config = {}
    class_instance = get_class_instance(
        'ScraperBase', config=config)
    assert hasattr(class_instance, '__class__')


def test_get_class_instance_fail():
    assert get_class_instance('WrongClass') is None


def test_call_class_method_pass():
    class_instance = get_class_instance(class_name='ScraperBase')
    assert call_class_method(
        class_instance, 'send_request', url='https://www.google.com', method='GET') is not None


def test_call_class_method_fail():
    class_instance = get_class_instance(
        class_name='ScraperBase')
    assert call_class_method(
        class_instance, 'missing_fn') is None
