import pytest
from utils.validators import validate_and_parse_url


def test_validate_and_parse_url():
	"""Tests the utility method for validating and parsing a url"""
	url = validate_and_parse_url(
		'https://www.google.com/search?q=How+to+run+python+tests&sourceid=chrome&ie=UTF-8')
	assert url.get('base', '') == 'www.google.com', 'url base should be equal to www.google.com'
	assert url.get('query', '') != '', 'Parsed url should have a query string'
