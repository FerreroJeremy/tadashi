import argparse

from tadashi.tadashi import Tadashi


def main():
    arg_parser = argparse.ArgumentParser(description='Context-aware deep decision system for smart home')
    arg_parser.add_argument('-l', '--location', help='Your city location', required=True)
    arg_parser.add_argument('-c', '--context', help='The context: your current activity in your house', default=None)
    args = arg_parser.parse_args()

    tadashi = Tadashi()
    tadashi.process(args.location, args.context)


if __name__ == '__main__':
    main()
