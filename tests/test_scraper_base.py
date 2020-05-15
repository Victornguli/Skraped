import pytest
# from fake_useragent import UserAgent
from skraped.scraper_base import ScraperBase


def test_send_requests_pass():
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Software+developer&sc.keyword=Software+developer&locT=N&locId=130&jobType="
    response = ScraperBase.send_request(url, 'get')
    assert response is not None
    assert 'Developer' in response


def test_send_requests_fail():
    url = "https://www.glassdoor.com/about/faq"
    response = ScraperBase.send_request(url, 'geT')
    # The above url declared as a dissalowed path  in the site's robots.txt
    assert response is None
