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
    lgr.critical('Initialized job Logs')
    config = parse_config()
    print(config)
    # validate_conf(config)
    # print(config.kw)
    return 'OK'


if __name__ == "__main__":
    main()
