import sys
import logging
from config.parser import parse_config
from config.validate_config import validate_conf


lgr = logging.getLogger(__name__)
lgr.setLevel('INFO')
logging.basicConfig(filename='basic.log', level='INFO')

if lgr.level == 20:
    lgr.addHandler(logging.StreamHandler(sys.stdout))
else:
    lgr.addHandler(logging.StreamHandler())


def main():
    config = parse_config()
    pass


if __name__ == "__main__":
    main()
