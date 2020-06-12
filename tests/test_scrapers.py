import pytest
from skraped import BrighterMonday, Glassdoor


@pytest.mark.parametrize("scraper_class", [Glassdoor, BrighterMonday])
def test_get_job_details(get_scraped_job_details):
    job_details = get_scraped_job_details
    assert job_details.get("title") != ""
