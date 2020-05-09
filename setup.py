from setuptools import setup, find_packages

from skraper import __version__ as version

description = 'CLI tool for scraping and aggregating Kenyan tech job posted on various job boards'
url = 'https://github.com/Victornguli/Skraped'
requires = [
	'pytest>=5.4.2',
	'coveralls-2.0.0',
]

with open("README.md", 'r') as f:
	long_description = f.read()

setup(
	name = 'Skraped',
	version = version,
	description = description,
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	author = 'Victor Nguli Joseph',
	author_email = 'victornjoseph@gmail.com',
	url = url,
	license = 'MIT License',
	python_requires = '>=3.6.0',
	install_requires = requires,
	packages = find_packages(exclude = 'tests'),
	include_package_data = True,
	entry_points = {'console_scripts': ['skraper=skraper.__main__:main']}
)
