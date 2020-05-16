import logging
import json
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

        pages = self.get_pages(page_limit=1)
        job_details = []

        if pages:
            job_links = self.get_job_links(pages)
            if not job_links:
                lgr.error(
                    'Failed to retrieve the job links for Glassdoor search')
                return job_details
            for link in job_links:
                lgr.info(f'Fetching details for {link}')
                info = self.extract_job_details(link)
                if not info:
                    lgr.error(f'Failed to retrieve details for {link}')
                    continue
                job_details.append(info)
            with open('details.json', 'a+') as f:
                json.dump(job_details, f)
                # lgr.info('Retrived {} pages from Glassdoor'.format(len(pages)))
        return len(job_details)

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
                lgr.info(f'Fetched page {page_count} of Glassdoor results')
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

    def get_job_links(self, pages_soup):
        """
        Retrieves job links from scraped pages
        @param pages_soup: The parsed HTML for each of the pages to be processed
        @type pages_soup: BeautifulSoup
        @return: List of the extracted job links
        @rtype: List
        """
        job_links = set()
        for page in pages_soup:
            links = page.find_all(
                'a', {'class': ['jobInfoItem', 'jobTitle', 'jobLink']})
            if links:
                links = map(lambda x: x['href'], links)
                for link in links:
                    if link not in job_links:
                        job_links.add(self.base_url + link)
        return list(job_links)

    def extract_job_details(self, job_url):
        """
        Extracts job details from each job link
        @param job_url: A link/url to the job details page
        @type job_url: str
        @return: The extracted job details
        """
        res = self.send_request(job_url, 'get')
        if not res:
            lgr.error(f'{job_url} details request returned None')
            return None
        soup = BeautifulSoup(res)
        if not soup:
            lgr.error(
                f'Failed to parse the response HTML for this post {job_url}')
            return None
        job_details = {
            'title': '',
            'company': '',
            'job_link': job_url,
            'application_link': '',
            'description': '',
            'job_id': ''
        }
        title = soup.find('div', {'class': 'e11nt52q5'})
        company = soup.find('div', {'class': 'e11nt52q1'})
        application_link = soup.find('a', {'class': 'applyButton'})
        description = soup.find('div', {'class': 'desc'})

        job_details['title'] = title.text if title else ''
        job_details['company'] = company.text if company else ''
        job_details['application_link'] = self.base_url + \
            application_link['href'] if application_link else ''
        job_details['description'] = description.text if description else ''
        job_details['job_id'] = application_link['data-job-id'] if application_link else ''

        return job_details
