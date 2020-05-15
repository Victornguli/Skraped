import logging
import sys


def configure_logging():
    lgr = logging.Logger('main')
    lgr.setLevel('INFO')
    logging.basicConfig(filename='basic.log', level='INFO')

    if lgr.level == 20:
        lgr.addHandler(logging.StreamHandler(sys.stdout))
    else:
        lgr.addHandler(logging.StreamHandler())
