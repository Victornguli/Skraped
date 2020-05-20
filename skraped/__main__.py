import os
import sys
import logging
import csv
from skraped.config.parser import parse_config
from skraped.config.validate_config import validate_conf
from skraped.scraper_base import ScraperBase
from skraped.glassdoor import Glassdoor
from skraped.brighter_monday import BrighterMonday


lgr = logging.getLogger()
lgr.setLevel('INFO')
logging.basicConfig(filename='basic.log', level='INFO')

if lgr.level == 20:
    lgr.addHandler(logging.StreamHandler(sys.stdout))
else:
    lgr.addHandler(logging.StreamHandler())


def main():
    config = parse_config()
    validate_conf(config)
    base = ScraperBase(config)
    scraper_classes = config.get('sources')
    # return config
    for scraper in scraper_classes:
        class_instance = get_class_instance(scraper, config=config)
        if class_instance is None:
            lgr.error(
                f'Failed to retrieve the Scraper Class {scraper}. Exiting...')
            sys.exit()
        scrape = get_class_method(class_instance, 'scrape')
        res = scrape()
        save_to_csv(res, config)


def get_class_instance(class_name, **kwargs):
    """Retrieves a class instance to be used for running individual scrapers"""
    if class_name in globals() and hasattr(globals()[class_name], '__class__'):
        try:
            return globals()[class_name](**kwargs)
        except TypeError:
            lgr.warning(f'{class_name} cannot be retrieved.')
    return None


def get_class_method(class_instance, function_name, **kwargs):
    """
    Retrives a class function from the passed in class instance
    """
    try:
        if class_instance is not None and function_name:
            return getattr(class_instance, function_name)
    except AttributeError:
        lgr.warning(
            f'method {function_name} does not exist in {class_instance}')
    return None


def save_to_csv(data, config):
    """
    Saves the job information list to the output csv file defined in the config
    @param job_info: A list of job dictionaries each containing the job details
    @type job_info: list
    @return: Status to indicate that the details had been saved. 
    """
    try:
        output_path = config.get('output_path')
        if not os.path.exists("{}/{}".format(output_path, '{}.csv'.format(output_path))):
            # Write CSV File and the Header row first..
            with open(os.path.join(output_path, '{}.csv'.format(output_path)), 'w+', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["TITLE", "COMPANY", "JOB LINK", "APPLICATION LINK", "DESCRIPTION", "JOB ID", "SOURCE"])
        lgr.info(
            f'\nWriting results to file at {output_path}/{output_path}.csv')
        csv_list = [[str(i['title']), str(i['company']), str(i['job_link']), i['application_link'], i['description'].encode(
            'ascii', 'ignore').decode('utf-8').replace("\t", "\n"), i['job_id'], i['source']] for i in data]
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


if __name__ == "__main__":
    main()
