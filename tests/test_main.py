import pytest
from skraper.__main__ import main


def test_main():
	res = main()
	assert res == 'OK', 'Dummy test should pass'
