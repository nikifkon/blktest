from argparse import ArgumentParser, FileType

from app.fio import measure


def main():
    """
    TODO
    """
    parser = ArgumentParser(
        prog="blktest",
        description=__doc__,
    )
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-f", "--filename", type=FileType("wb"), required=True)
    parser.add_argument("-o", "--output", type=FileType("wb"), required=True)
    args = parser.parse_args()
    results = measure(args)


if __name__ == "__main__":
    main()
