import pytest
from unittest import TestCase
from skraped.utils import validate_and_parse_url, get_job_id


class TestUtils(TestCase):
    def setUp(self):
        """Setup various variables to be used across the test class"""
        self.pass_url = 'https://www.google.com/search?q=How+to+run+python+tests&sourceid=chrome&ie=UTF-8'
        self.fail_url = "www.google"
        self.glass_job_url = "https://www.glassdoor.com/partner/jobListing.htm?pos=103&ao=4120&s=58&guid=00000172483cdc0f9bc1921f285401d9&" +\
        "src=GD_JOB_AD&t=SR&extid=1&exst=OL&ist=&ast=OL&vt=w&slr=true&ea=1&cs=1_94a187d8&cb=1590349847898&jobListingId=3226944700"
        self.brighter_job_url = "https://www.brightermonday.co.ke/job/ict-intern-q75qv4"

    def test_validate_and_parse_url_pass(self):
        url = validate_and_parse_url(self.pass_url)
        assert url is not None, "Should not fail url validation and parsing"
        assert url.get('base', '') == 'www.google.com', 'url base should be equal to www.google.com'

    def test_validate_and_parse_url_fail(self):
        malformed_url = validate_and_parse_url(self.fail_url)
        assert malformed_url is None, 'url validation and parsing shoul fail'

    def test_get_job_id_pass(self):
        glassdoor_id = get_job_id(self.glass_job_url, source = "glassdoor")
        brighter_id = get_job_id(self.brighter_job_url, source = "brightermonday")
        assert glassdoor_id == "3226944700", "Should return appropriate job_id for the job link"
        assert brighter_id == "q75qv4", "Should return appropriate job_id for the job link"

    def test_get_job_id_fail(self):
        glassdoor_id = get_job_id(self.glass_job_url, source = "glassddoor")
        get_id_fail = get_job_id("thisisnotaurl", source = "somesauce")
        assert glassdoor_id is None, "Should fail because of invalid source identifier"
        assert get_id_fail is None, "Should fail because an ivalid url was passed"
