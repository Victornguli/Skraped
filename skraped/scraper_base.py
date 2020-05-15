import logging
import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

lgr = logging.getLogger(__name__)

# TODO: Add a base requests method/config to be used by each scraper class


class ScraperBase():
    """Base class implementing core scraping functionality"""

    def __init__(self, config={}):
        self.config = config

    def scrape(self):
        """Entry Point to the execution of all scrape scources defined in the config"""
        scraper_classes = self.config.sources
        for scraper_class in scraper_classes:
            class_instance = self.get_class_instance(
                scraper_class, config=self.config)
            self.call_class_method(
                class_instance, 'scrape', config=self.config)

    def get_next_page(self, *args, **kwargs):
        raise NotImplementedError

    def extract_jobs_from_page(self, *args, **kwargs):
        raise NotImplementedError

    def extract_jobs_from_details(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def send_request(url, method):
        """Sends an http request to the url using requests library"""
        try:
            ua = UserAgent()
            headers = {
                'User-Agent': ua.random,
                'Accept-Language': 'en-GB',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': 'https://www.google.co.ke',
            }
            # TODO: Add proxy mechanism.
            proxies = {
                'https': ''
            }
            # Pass empty proxies for now. Allow calling of diffrent HTTP methods separately.
            req = requests.get  # Defaults the HTTP method to get
            try:
                req = getattr(requests, method)
            except AttributeError:
                lgr.warning(
                    f'{method} is an invalid HTTP method. Defaulting to GET')
            resp = req(url, proxies=proxies, headers=headers, timeout=10)
            if resp.status_code != 200:
                lgr.error(
                    f'Request to {url} return status code {resp.status_code}')
            else:
                return resp.text
        except requests.ConnectionError as e:
            lgr.error(
                'Connection Error. Make sure that you are connected to the internet and try again')
            print(str(e))
        except requests.Timeout as e:
            lgr.error(
                'Timeout Error. Adjust your timeout value or try again later if this issue persists')
        except requests.RequestException as e:
            lgr.error(f'{method} request to {url} failed.')
            print(str(e))
        return None
