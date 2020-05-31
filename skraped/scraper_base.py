import os
import csv
import pickle
import requests
import logging
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from .utils import validate_and_parse_url, get_job_id

lgr = logging.getLogger()


class ScraperBase():
    """Base class implementing core scraping functionality"""

    def __init__(self, config={}):
        self.config = config
        self.output_path = self.config.get('output_path')
        self.delay = self.config.get('delay', False)
        self.min_delay  = self.config.get('delay_range', {}).get('min_delay', 0)
        self.max_delay  = self.config.get('delay_range', {}).get('max_delay', 10)

    def scrape(self):
        """
        Entry Point to the execution of all scrape scources defined in the config
        """
        raise NotImplementedError

    def save_csv(self, scrape_data):
        """
        Saves scraped data to a csv file within the output path defined in config
        @param scrape_data: A list of job dictionaries each containing the job details
        @type scrape_data: list
        @return: Boolean to indicate that the status of the operation.
        """
        try:
            if scrape_data:
                with open(os.path.join(self.output_path, "data.csv"), "w", encoding='utf-8') as f:
                    fieldnames = ["TITLE", "COMPANY", "JOB LINK",
                                "APPLICATION LINK", "DESCRIPTION", "JOB ID", "SOURCE"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in scrape_data:
                        data = {
                            "TITLE": row["title"], "COMPANY": row["company"], "JOB LINK": row["job_link"],
                            "APPLICATION LINK": row["application_link"], "DESCRIPTION": row["description"],
                            "JOB ID": row["job_id"], "SOURCE": row["source"]
                        }
                        writer.writerow(data)
                lgr.info(f"Saved results to {self.output_path} successfully.")
                return True
        except Exception as e:
            lgr.error(
                f'\nFailed to save search results in csv file. Output path {self.output_path}')
            print(str(e))
        return False

    def load_csv(self):
        """
        Loads existing csv file from the path specified in the config
        @return: Saved csv data
        @rtype: list | None
        """
        saved_data = []
        try:
            with open(os.path.join(self.output_path, "data.csv"), "r", encoding="utf-8") as saved_csv:
                fieldnames = [
                    "TITLE", "COMPANY", "JOB LINK", "APPLICATION LINK", "DESCRIPTION", "JOB ID", "SOURCE"]
                csv_reader = csv.DictReader(saved_csv, fieldnames=fieldnames)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:  # Skip header row
                        line_count += 1
                        continue
                    saved_data.append({
                        "title": row["TITLE"], "company": row["COMPANY"], "job_link": row["JOB LINK"],
                        "application_link": row["APPLICATION LINK"], "description": row["DESCRIPTION"],
                        "job_id": row["JOB ID"], "source": row["SOURCE"]})
                    line_count += 1
            return saved_data
        except FileNotFoundError:
            lgr.info(f"No existing csv file found {self.output_path}")
        return saved_data

    def save_pickle(self, scrape_data):
        """
        Saves scraped data in pickle format for easier filtering and restoring deleted csv files.
        @param scraped_data: The list of scraped jobs
        @type scraped_data: list
        @return: Boolean to indicate the status of save pickle operation
        @rtype: bool
        """
        try:
            if scrape_data:
                with open(os.path.join(self.output_path, "data.pkl"), "wb") as pickle_file:
                    pickle.dump(scrape_data, pickle_file)
                lgr.info(
                    f"Dumped scraped pickle at {self.output_path} successfully")
        except Exception as ex:
            lgr.error(
                f"Failed to save pickle data at {self.output_path}")
            print(str(ex))
        return False

    def load_pickle(self):
        """
        Loads scraped data from saved pickles.
        @return: Scraped data dumped in the pickle
        @rtype: list | None 
        """
        scrape_data = []
        try:
            with open(os.path.join(self.output_path, "data.pkl"), "rb") as pickle_file:
                scrape_data = pickle.load(pickle_file)
            lgr.info(
                f"Loaded scrape_data from pickle at {self.output_path} successfully")
            return scrape_data
        except Exception as ex:
            lgr.error(
                f"Failed to load scrape_data from pickle data at {self.output_path}")
            print(str(ex))
        return scrape_data

    def merge_scrape_data(self, scrape_data):
        """
        Merges scraped data with data from the saved csv   
        @param scrape_data: Current scrape data
        @type scrape_data: list
        @return: Merged scrape data. Avoids saving data with duplicate ids to the csv file
        @rtype: list
        """
        try:
            if scrape_data:
                csv_data = self.load_csv()
                dups = dict((i["job_id"], i) for i in csv_data) if csv_data else {}
                for job in scrape_data:
                    dups[job["job_id"]] = job
                scrape_data = [dups[key] for key in dups]
                return scrape_data
        except Exception as ex:
            lgr.error("Failed to merge scraped data")
            print(str(ex))
        return scrape_data

    def run_pre_scrape_filters(self, job_links, source):
        """
        Runs filters for job links before scraping each job post.
        @param job_links: List of job links scraped from the search result pages
        @type job_links: list
        @return: Filtered job_links list
        @param source: The job link source
        @type source: str
        @rtype list 
        """
        res = []
        job_ids = dict((get_job_id(job_link, source), job_link) for job_link in job_links)
        try:
            ids = [job["job_id"] for job in self.load_csv() if job["source"] and job["source"].lower() == source]
            res = [job_ids[job_id] for job_id in job_ids if job_id not in ids and job_id is not None]
            dups = len(job_ids) - len(res) 
            lgr.info("Found {} saved ids out of the {} scraped ids for source {} \n".format(dups, len(job_ids), source))
            return res
        except Exception as e:
            lgr.info("Failed to filter job_ids")
            print(str(e))
        return res

    @staticmethod
    def send_request(url, method, return_raw=False):
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
            req = requests.get  # Defaults the HTTP method to get
            try:
                req = getattr(requests, method.lower())
            except AttributeError:
                lgr.warning(
                    f'{method} is an invalid HTTP method. Defaulting to GET')
            resp = req(url, proxies=proxies, headers=headers, timeout=10)
            if resp.status_code != 200:
                lgr.error(
                    f'Request to {url} return status code {resp.status_code}')
            else:
                return resp if return_raw else resp.text
        except requests.ConnectionError as e:
            lgr.error(
                'Connection Error. Make sure that you are connected to the internet and try again')
            print(str(e))
        except requests.Timeout as e:
            lgr.error(
                'Request timed out. Adjust your timeout value or try again later if this issue persists')
        except requests.RequestException as e:
            lgr.error(f'{method} request to {url} failed.')
            print(str(e))
        return None

    def process_job_details(self, class_instance, target_method, job_links, **kwargs):
        """
        Manages a pool of multi-threaded calls to each job_link scraper function
        @param class_instance: The instance of the scraper class calling this method
        @type class_instance: class
        @param target_method: The method for scraping the job link. Implemented within each scraper class
        @type target_method: str
        @param job_links: List of job_links to be scraped
        @type job_links: list
        @param kwargs: Extra key-value pair args to be passed to the target method
        """
        if job_links:
            with ThreadPoolExecutor() as executor:
                try:
                    method_instance = getattr(class_instance, target_method)
                except AttributeError as e:
                    lgr.error(f"Method {target_method} does not exist in {class_instance} scraper class")
                    print(e)
                else:
                    results = []
                    futures = [executor.submit(method_instance, link, delay = random.randrange(self.min_delay, self.max_delay) if self.delay else 0, **kwargs) for link in job_links]
                    for future in as_completed(futures):
                        res = future.result()
                        results.append(res)
                    getattr(class_instance, 'scrape_data').extend(results) # Extend scrape_data instance for that scraper class
        return
