# Skraped!

[![Coverage Status](https://coveralls.io/repos/github/Victornguli/Skraped/badge.svg)](https://coveralls.io/github/Victornguli/Skraped)
[![Build Status](https://travis-ci.com/Victornguli/Skraped.svg?branch=master)](https://travis-ci.com/Victornguli/Skraped)

Scraped is a command line tool that scrapes and aggregates job from several Kenyan job sites. These scraped job posts
 are saved in a csv file that allows a job seeker to conveniently review jobs from several sources.
 
## Getting Started

These instructions will get you a copy of Skraper running on your local machine for development and testing purposes.

#### Dependencies

Skraper requires [Python 3.6.0](https://www.python.org) or a later version. Other library dependencies have been
 declared within setup.py and will be automatically installed when installing the project using setup
 
#### Installation
```
pip install git+https://github.com/Victornguli/Skraped.git
skraper --help
```

or for testing purposes you can first clone the repository then install skraped via setup.py

```
git clone https://github.com/Victornguli/Skraped.git skraped
cd skraped
python setup.py install
skraper --help
```

### Using Skraped
To run a scrape session initialize the scraper with the keywords arguments and an output path(Where the scrape data and pickle backups will be saved)
NOTE THAT the output directory is relative to the directory you are running skraper from, 
unless explicitly declared as absolute like **/home/{{username}}/jobsearch**
```
skraper -o devjobs -kw "Software developer"
```

This will run and create a directory devjobs relative to current directory, scrape the sites enabled on skraped/config/settings.yaml
and save the scraped data in a csv file as well as pickle format backups


### Extra Configuration
To customize your experience you can supply additional arguments when running the scraper or define them in a settings.yaml file located in
skraped/config/settings.yaml. You can override this file by copying the default file, updating it with your own configuration values and running the 
scraper with **-s** flag supplying the location of the config file. Example

```
skraper -o /home/{{your_username}}/jobsearch -s /home/{{your_username}}/jobsearch/custom_settings.yaml
```

Under yaml settings file you can configure the following options

| Option      | Type         | Description                                                                                |
|-------------|--------------|--------------------------------------------------------------------------------------------|
| output_path | string       | Path where scraped data will be saved                                                      |
| sources     | List[string] | List of sources to be scraped. Comment out a source  to ignore it when running the scraper |
| keywords    | string       | The keywords to be used when running the job searches from  the sources                    |
| delay       | boolean      | If enabled will add a reasonable or random delay to the spiders to avoid rate limiting     |



### Local development
If you use the setup.py instal method, you will need to run **python setup.py install** to update the skraper egg binary on ANY SOURCE CODE
CHANGES so that the command **skraper** can run the latest version within your virtualenvironment

**Goodluck in your job search :)**
