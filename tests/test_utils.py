import pytest
from skraped.utils import validate_and_parse_url
from skraped.scraper_base import ScraperBase


def test_validate_and_parse_url():
    """Tests the utility method for validating and parsing a url"""
    url = validate_and_parse_url(
        'https://www.google.com/search?q=How+to+run+python+tests&sourceid=chrome&ie=UTF-8')
    malformed_url = validate_and_parse_url(1)
    assert url.get(
        'base', '') == 'www.google.com', 'url base should be equal to www.google.com'
    assert malformed_url is None, 'Malformed url should return None'
