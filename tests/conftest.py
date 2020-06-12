import pytest
from skraped import ScraperBase, BrighterMonday, Glassdoor


@pytest.fixture
def scraper_base_instance(valid_config):
    return ScraperBase(valid_config)


@pytest.fixture
def valid_config(tmpdir):
    return {
        'output_path': tmpdir, 'sources': ['Glassdoor', 'BrighterMonday'],
        'keywords': 'Software Developer', 'delay': True,
        'delay_range': {'min_delay': 2, 'max_delay': 10}}


@pytest.fixture
def scrape_data():
    return [{
        "title": "Software Engineer",
        "company": "Finplus Group",
        "job_link": "https://www.glassdoor.com/partner/jobListing.htm?pos=104&ao=46442&s=58&guid=000001726fdc717096d2510655e55dcc&src=GD_JOB_AD&t=SR&extid=1&exst=OL&ist=&ast=OL&vt=w&slr=true&cs=1_7681ce45&cb=1591014617726&jobListingId=3588366071",
        "application_link": "https://finplusgroup.breezy.hr/p/b3fcafde37b3-20205?source=glassdoor",
        "description":
        """
        Role Description
        This is a hands-on software development role. It will encompass all aspects of 
        the software development life-cycle working with a small engineering team and demands a high understanding of application design and architecture.
        
        Key Responsibilities
        Work with the Engineering team in developing the whole suite of Finplus Group products (web, mobile apps, sms, USSD).
        Be a major contributor to the Agile Software Methodology which we use at Finplus Group
        Work with partners on integrations that will require involvement in all aspects of the software development cycle from requirement analysis to implementation
        Develop software using our development stack which includes Ruby on Rails, Postgresql, Android, Apache, Phusion Passenger, Ubuntu Linux, AWS, jQuery, Angular.js, Bootstrap and use tools such as JIRA, Bitbucket, Jenkins, Redis among others.
        Interfacing with clients to understand their business, goals and visions for products and solutions being supported by Finplus Group.
        """,
        "job_id": "3588366071",
        "source": "Glassdoor"
    }]


@pytest.fixture
def job_links():
    return [
        "https://www.glassdoor.com/partner/jobListing.htm?pos=104&ao=46442&s=58&guid=000001726fdc717096d2510655e55dcc&src=GD_JOB_AD&t=SR&extid=1&exst=OL&ist=&ast=OL&vt=w&slr=true&cs=1_7681ce45&cb=1591014617726&jobListingId=3588366071",
        "https://www.glassdoor.com/partner/jobListing.htm?pos=113&ao=46442&s=58&guid=000001726fdc717096d2510655e55dcc&src=GD_JOB_AD&t=SR&extid=1&exst=OL&ist=&ast=OL&vt=w&slr=true&cs=1_3ddf1d30&cb=1591014617733&jobListingId=3588370830",
        "https://www.glassdoor.com/partner/jobListing.htm?pos=107&ao=46442&s=58&guid=000001726fdc717096d2510655e55dcc&src=GD_JOB_AD&t=SR&extid=1&exst=OL&ist=&ast=OL&vt=w&slr=true&cs=1_4ccec5e5&cb=1591014617729&jobListingId=3588360729"
    ]


@pytest.fixture
def saved_csv(valid_config, scrape_data):
    def save_to_csv():
        s = ScraperBase(valid_config).save_csv(scrape_data)
        return s is True
    return save_to_csv


@pytest.fixture
def get_scraped_pages(valid_config, scraper_class):
    class_instance = scraper_class(valid_config)
    class_instance.build_url()
    class_instance.get_pages()
    return class_instance


@pytest.fixture
@pytest.mark.parametrize("scraper_class", [Glassdoor, BrighterMonday])
def get_scraped_job_details(get_scraped_pages):
    scraper_instance = get_scraped_pages
    assert scraper_instance.pages != [], "Should fetch search result pages"
    links = scraper_instance.get_job_links(scraper_instance.pages)
    link = links[0] if links else None
    assert link is not None, "Should retrieve the job_link"
    details = scraper_instance.extract_job_details(link)
    return details
