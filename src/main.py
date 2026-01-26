import logging

from data.Loader import Loader
from utils import cli, logger


def main():
    args = cli.parse_arguments()

    logger.init_logger(args.trace)

    _LOGGER = logging.getLogger(__name__)

    data = Loader.load(args.path)


if __name__ == '__main__':
    main()
