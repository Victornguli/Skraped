"""
Common utility functions
"""
import os
import logging
import validators
from urllib.parse import urlparse
from datetime import datetime
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
        lgr.info(f'Failed to parse url {url}')
        return None
    if source.lower() == "glassdoor":
        job_url = parsed_url.get("query")
        if job_url:
            # Retrieve each query_param as key:val pairs
            try:
                parsed_params = dict(x.split("=") for x in job_url.split('&'))
                if parsed_params:
                    return parsed_params.get("jobListingId", None)
            except IndexError:  # pragma: nocover
                pass
    elif source.lower() == "brightermonday":
        try:
            return parsed_url.get("path").split("-")[-1]
        except IndexError:  # pragma: nocover
            pass
    return None


def parse_pickle_name(pickle_date=None):
    """
    Parses picle name from input date strings or returns the current pickle name if no
    date is not passed
    @param pickle_date: The date the pickle was created
    @type pickle_date: str | None
    @return: pickle_name
    @rtype: str | None
    """
    if pickle_date:
        pickle_name = datetime.strptime(pickle_date, "%m-%d-%Y").date().strftime("%m-%d-%Y")
    else:
        today = datetime.now().date()
        pickle_name = today.strftime("%m-%d-%Y")
    return f"{pickle_name}.pkl"
