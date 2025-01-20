import logging
from argparse import ArgumentParser, FileType
from app.fio import measure
from app.plot import plot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser(prog="blktest")
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-f", "--filename", type=FileType("wb"), required=True)
    parser.add_argument("-o", "--output", type=FileType("wb"), required=True)
    args = parser.parse_args()
    logger.info(args)
    results = measure(args)
    logger.info(results)
    plot(results, args.output)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.error(exc)
        exit(1)
