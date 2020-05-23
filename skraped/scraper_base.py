import os
import csv
import pickle
import requests
import logging

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

lgr = logging.getLogger()

# TODO: Add a base requests method/config to be used by each scraper class


class ScraperBase():
    """Base class implementing core scraping functionality"""

    def __init__(self, config={}):
        self.config = config
        self.output_path = self.config.get('output_path', '')

    def scrape(self):
        """
        Entry Point to the execution of all scrape scources defined in the config
        """
        raise NotImplementedError

    def save_to_csv(self, scrape_data):
        """
        Saves scraped data to a csv file within the output path defined in config
        @param scrape_data: A list of job dictionaries each containing the job details
        @type scrape_data: list
        @return: Boolean to indicate that the status of the operation.
        """
        try:
            output_path = self.output_path
            if not os.path.exists("{}/{}".format(output_path, '{}.csv'.format(output_path))):
                # Write CSV File and the Header row first..
                with open(os.path.join(output_path, '{}.csv'.format(output_path)), 'w+', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        ["TITLE", "COMPANY", "JOB LINK", "APPLICATION LINK", "DESCRIPTION", "JOB ID", "SOURCE"])
            lgr.info(
                f'\nWriting results to file at {output_path}/{output_path}.csv')
            csv_list = [[str(i['title']), str(i['company']), str(i['job_link']), i['application_link'], i['description'].encode(
                'ascii', 'ignore').decode('utf-8').replace("\t", "\n"), i['job_id'], i['source']] for i in scrape_data]
            with open(os.path.join(output_path, '{}.csv'.format(output_path)), 'a+', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(csv_list)
            lgr.info(f'\nSaved results')
            return True
        except Exception as e:
            lgr.error(
                f'\nFailed to save search results in csv file. Output path {output_path}')
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
            with open(f"{self.output_path}/{self.output_path}.csv", "r") as saved_csv:
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
                lgr.info(
                    "Read {} lines from {}".format(line_count - 1, self.output_path))
            return saved_data
        except Exception as ex:
            lgr.error(f"Failed to read csv file at {self.output_path}")
            print(str(ex))
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
            with open(f"{self.output_path}/{self.output_path}.pkl", "wb") as pickle_file:
                pickle.dump(pickle_file, scrape_data)
            lgr.info(
                f"Dumped scraped pickle at {self.output_path} successfully")
        except Exception as ex:
            lgr.error(f"Failed to save pickle data at {self.output_path}")
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
            with open(f"{self.output_path}/{self.output_path}.pkl", "rb") as pickle_file:
                scrape_data = pickle.load(pickle_file)
            lgr.info(
                f"Loaded scrape_data from pickle at {self.output_path} successfully")
            return scrape_data
        except Exception as ex:
            lgr.error(
                f"Failed to load scrape_data from pickle data at {self.output_path}")
            print(str(ex))
        return scrape_data

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
