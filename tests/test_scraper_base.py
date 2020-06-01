import pytest
# from fake_useragent import UserAgent
from skraped.scraper_base import ScraperBase

@pytest.fixture
def scraper_base_instance(valid_config):
    return ScraperBase(valid_config)

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

def test_load_csv(valid_config, scrape_data):
    csv_save = ScraperBase(valid_config).save_csv(scrape_data)
    assert csv_save is True
    assert ScraperBase(valid_config).load_csv() != []

def test_load_pickle(valid_config, scrape_data):
    pickle_save = ScraperBase(valid_config).save_pickle(scrape_data)
    assert pickle_save is True
    assert ScraperBase(valid_config).load_pickle() != []

def test_run_pre_scrape_filters(job_links, saved_csv, valid_config):
    assert saved_csv() is True
    pre_filter = ScraperBase(valid_config).run_pre_scrape_filters(job_links, "glassdoor")
    assert len(pre_filter) == 2, "Should filter out existing job_ids from the returned job_links"

def test_merge_scrape_data(scraper_base_instance, saved_csv, scrape_data):
    # assert saved_csv() is True
    assert scraper_base_instance.merge_scrape_data(scrape_data) != []
