"""
Common validator utility functions
"""
import logging
from urllib.parse import urlparse


def validate_and_parse_url(url):
	"""
	Validates and parse a url string to return appropriate url parts e.g scheme, base url, etc
	:param url: The url string to be validated and parsed
	:type url: str
	:return: str | None
	"""
	try:
		parsed_url = urlparse(url)
		return {
			'scheme': parsed_url.scheme, 'base': parsed_url.netloc, 'path': parsed_url.path, 'params':
				parsed_url.params, 'query': parsed_url.query}
	except Exception as ex:
		logging.exception('validate_and_parse_url Exception: %s' % ex)
	return None
