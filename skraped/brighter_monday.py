import logging
from bs4 import BeautifulSoup
from skraped.scraper_base import ScraperBase
from skraped.utils import validate_and_parse_url

lgr = logging.getLogger()


class BrighterMonday(ScraperBase):
    """Scraper class for scraping Brighter Monday jobs"""

    def __init__(self, config={}):
        super().__init__(config)
        self.base_url = 'https://www.brightermonday.co.ke'
        self.alturl = 'https://www.brightermonday.co.ke/jobs'
        # Provides accurate results for IT Jobs
        self.url = 'https://www.brightermonday.co.ke/jobs/it-software'
        self.query_params = {
            'page': 1,
            'q': self.config.get('keywords', '')
        }
        self.extra_headers = {}
        self.page_limit = 1

    def scrape(self):
        """Entry point for the scraper"""
        main_query = self.query_params.popitem()
        self.url += '?' + main_query[0] + '=' + \
            ("+").join(main_query[1].split(" "))
        for param in self.query_params:
            if param != 'page':
                self.url += "&" + param + "=" + \
                    ("+").join(self.query_params[param].split(" "))

        pages = self.get_pages(self.page_limit)
        if not pages:
            lgr.error('Failed to retrieve any Brighter Monday results page')
            return None

        job_links = self.get_job_links(pages)
        if not job_links:
            lgr.error(
                'Failed to retrieve any jobs link for Brighter Monday page results')
        res = []
        for link in job_links:
            if link:
                link_res = self.extract_job_details(link)
                res.append(link_res)
        return res

    def get_pages(self, page_limit=1):
        """
        Retrieves each job results page upto the specified limit. 
        Tries to fetch the first page then subsequent page calls are done if 
        number of processed_pages remain to be lesser than the page_limit defined 
        @param page_limit: The page limit to be applied when retrieving the pages
        @type page_limit: int
        """
        processed_pages = 0
        pages = []
        res = self.send_request(self.url, 'get')
        if res is not None:
            soup = BeautifulSoup(res, 'lxml')
            pages.append(soup)
            processed_pages += 1
            lgr.info(
                f'Fetched page {processed_pages} of Brighter Monday results')
        if processed_pages:
            while processed_pages < page_limit:
                res = self.send_request('{}&page={}'.format(
                    self.url, processed_pages + 1), 'get')
                if res is None:
                    lgr.info(
                        'Brighter Monday page retrieval Done. Retrieved {} out of {}(limit) pages'.format(processed_pages, page_limit))
                    break
                soup = BeautifulSoup(res, 'lxml')
                pages.append(soup)
                processed_pages += 1
                lgr.info(
                    f'Fetched page {processed_pages} of Brighter Monday results')

        return pages

    def get_job_links(self, pages_soup):
        """
        Retrieves job links from scraped pages. Searches for prerender link tags first and fallbacks
        to searching through the parsed HTML(soup) of each page.
        @param pages_soup: The parsed HTML for each of the pages to be processed
        @type pages_soup: BeautifulSoup
        @return: List of the extracted job links
        @rtype: List
        """
        job_links = []
        for page_idx, page in enumerate(pages_soup):
            # Search for prerender links first..
            link_tags = page.find_all('link', {'rel': 'prerender'})
            links = [tag['href'] for tag in link_tags if hasattr(tag, 'href')]
            if not links:
                lgr.info(
                    'Job link fetch using prerender links for Brighter Monday page {} failed.. Switching to parsed html'.format(page_idx + 1))
                job_containers = page.find_all(
                    'article', {'class': 'search-result'})
                if not job_containers:
                    lgr.error(
                        'Job links fetch for brighter monday page {} using parsed Html failed'.format(page_idx + 1))
                    continue  # Well nothing else can be done now..
                try:
                    links = [container.find('a')['href']
                             for container in job_containers]
                except Exception:
                    lgr.error(
                        'Job links for Brighter Monday page {} could not be extracted..'.format(page_idx + 1))
                else:
                    if not links:
                        lgr.error(
                            'Zero job links for Brighter Monday page {} retrieved'.format(page_idx + 1))
                        continue  # Again, nothing can be done past here.. just continue to the next, albeit with much skepticism :)
            # I'm presuming by now links list for a single page is not empty.. :)
            job_links.extend(links)
        return job_links

    def extract_job_details(self, job_url):
        """
        Extracts job details from each job link
        @param job_url: A link/url to the job details page
        @type job_url: str
        @return: The extracted job details
        """
        res = self.send_request(job_url, 'get', return_raw=True)
        if not res:
            lgr.error(f'Get job details for {job_url} failed')
            return None
        soup = BeautifulSoup(res.text, 'lxml')
        if not soup:
            lgr.error(
                'BeautifulSoup raw html parse using lxml for {job_url} failed')
            return None
        job_details = {
            'title': '',
            'company': '',
            'job_link': job_url,
            'application_link': job_url,
            'description': '',
            'job_id': '',
            'source': 'BrighterMonday'
        }
        title = soup.find('h1', {'class': 'job-header__title'})
        company = soup.find(
            'div', {'class': ['if-wrapper-column', 'job-header__details']}).find('h2').find('a')
        top_details = soup.find(
            'div', {'class': 'customer-card__content-segment'})
        description = soup.find(
            'div', {'class': 'description-content__content'})
        url_path = validate_and_parse_url(job_url)['path']
        job_id = url_path.split("-")[-1] if url_path else None

        job_details['title'] = title.text if title else ''
        job_details['company'] = company.text if company else ''
        job_details['description'] = top_details.text if top_details else ''
        job_details['description'] += description.text if description else ''
        job_details['job_id'] = job_id

        lgr.info(f'Success: Fetched details for {job_url}')
        return job_details
