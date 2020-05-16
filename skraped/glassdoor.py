import logging
from bs4 import BeautifulSoup
from skraped.scraper_base import ScraperBase

lgr = logging.getLogger()


class Glassdoor(ScraperBase):
    """Glasdoor scraper class"""

    def __init__(self, config={}):
        self.config = config
        super().__init__(config)
        self.base_url = 'https://www.glassdoor.com'
        self.url = 'https://www.glassdoor.com/Job/jobs.htm?'
        self.query_params = {
            'suggestCount': '0',
            'suggestChosen': 'false',
            'clickSource': 'searchBtn',
            'typedKeyword': self.config.get('keywords'),
            'locT': 'N',
            'locId': '130',
            'jobType': ''
        }

    def scrape(self):
        """
        Entry point for scraping Glassdoor
        """
        first_query = self.query_params.popitem()
        self.url += str(first_query[0])+'=' + str(first_query[1])
        for key, value in self.query_params.items():
            self.url += '&' + str(key)+'='+str(value)

        pages = self.get_pages(page_limit=5)
        lgr.info('Retrived {} pages from Glassdoor'.format(len(pages)))
        return len(pages)

    def get_pages(self, page_limit=2):
        """
        Retrieves each page upto the limit or last page if limit exceeds this.
        @param page_limit: The page limit to be applied when retrieving the pages
        @type page_limit: int
        """
        pages, page_count = [], 0
        next_page_url = self.url
        for _ in range(page_limit):
            res = self.send_request(next_page_url, 'get')
            if res is not None:
                page_soup = BeautifulSoup(res, 'lxml')
                pages.append(page_soup)
                page_count += 1
                footer = page_soup.find(
                    'div', {'id': 'FooterPageNav', 'class': 'pageNavBar'})
                if footer:
                    next_page_url = footer.find(
                        'li', {'class': 'next'}).find('a')['href']
                    if not next_page_url:
                        break
                    next_page_url = self.base_url + next_page_url
                else:
                    break
        return pages

    def get_job_links(self, soup):
        """
        Retrieves job links from scraped pages
        @param soup: The parsed HTML for the pages to be processed
        @type soup: BeautifulSoup
        @return: List of the extracted job links
        @rtype: List
        """
        job_links = list()
        pass

    def extract_job_details(self, job_url):
        """
        Extracts job details from each job link
        @param job_url: A link/url to the job details page
        @type job_url: str
        @return: The extracted job details
        """
        pass
