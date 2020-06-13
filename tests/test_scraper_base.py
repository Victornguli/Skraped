import pytest
from skraped import ScraperBase, BrighterMonday


def test_send_requests_pass():
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Software+developer&sc.keyword=Software+developer&locT=N&locId=130&jobType="
    response = ScraperBase.send_request(url, 'get')
    assert response is not None
    assert 'Developer' in response


def test_send_requests_fail():
    url = "https://www.glassdoor.com/about/faq"
    response = ScraperBase.send_request(url, 'geT')
    assert response is None


def test_load_csv(valid_config, scrape_data):
    csv_save = ScraperBase(valid_config).save_csv(scrape_data)
    assert csv_save is True
    assert ScraperBase(valid_config).load_csv() != []


def test_load_pickle(valid_config, scrape_data):
    pickle_save = ScraperBase(valid_config).save_pickle(scrape_data)
    assert pickle_save is True
    assert ScraperBase(valid_config).load_pickle() != []

def test_recover_scraped_data(valid_config, scrape_data):
    base = ScraperBase(valid_config)
    pickle_save = base.save_pickle(scrape_data)
    assert pickle_save is True, "Should save the pickle successfully"
    base.recover_scraped_data()
    data = base.load_csv()
    assert data[0].get('job_id') == scrape_data[0].get('job_id'), \
        "The recovered data must be equal to the one in scrape_data"

def test_run_pre_scrape_filters(job_links, saved_csv, valid_config):
    assert saved_csv() is True
    pre_filter = ScraperBase(valid_config).run_pre_scrape_filters(
        job_links, "glassdoor")
    assert len(pre_filter) == 2, \
        "Should filter out existing job_ids from the returned job_links"


def test_merge_scrape_data(scraper_base_instance, saved_csv, scrape_data):
    assert scraper_base_instance.merge_scrape_data(scrape_data) != []


def test_process_job_details():
    pass
