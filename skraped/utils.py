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


def get_job_id(url, source):
    """
    Retrieves a job_id from the job url. Works for sources which job links have the job_id as a param
    @param url: The job link to extract job id from
    @type url: str
    @param source: The job source identifier
    @type source: str
    @return: The extracted job_id or None if not found
    @rtype: str | None
    """
    parsed_url = validate_and_parse_url(url)
    if parsed_url is None:
        return None
    if source == "glassdoor":
        job_url = parsed_url.get("query")
        if job_url:
            # Retrieve each query_param as key:val pairs
            try:
                parsed_params = dict(x.split("=") for x in job_url.split('&'))
                if parsed_params:
                    return parsed_params.get("jobListingId", None)
            except IndexError:
                pass
    elif source == "brightermonday":
        try:
            return parsed_url.get("path").split("-")[-1]
        except IndexError:
            pass
    return None
