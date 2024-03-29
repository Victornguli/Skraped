from setuptools import setup, find_packages

# import from skraped package triggers imports of other modules unavailable during setup install
# from skraped import __version__ as version
version = '0.0.1'

description = 'CLI tool for scraping and aggregating Kenyan tech job posted on various job boards'
url = 'https://github.com/Victornguli/Skraped'
requires = [
    'pytest>=5.4.2',
    'pytest-cov>=2.8.1',
    'coveralls>=2.0.0',
    'validators>=0.15.0',
    'pyyaml>=5.3.1',
    'beautifulsoup4>=4.9.0',
    'lxml>=4.5.0',
    'fake-useragent>=0.1.11'
]

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='Skraped',
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Victor Nguli Joseph',
    author_email='victornjoseph@gmail.com',
    url=url,
    license='MIT License',
    python_requires='>=3.6.0',
    install_requires=requires,
    packages=find_packages(exclude=['tests']),
    package_data={
        # Install settings.yaml for loading default settings
        'skraped': ["config/*.yaml"]
    },
    include_package_data=True,
    entry_points={'console_scripts': ['skraper=skraped.__main__:main']}
)
