#!/usr/bin/env python
from components.base import build_component
import local_settings as settings
import argparse
import logging


def main():
    COMPONENT_TYPE_CHOICES = ['article', 'all', 'debug', 'author']
    parser = argparse.ArgumentParser(
            description="Converts Drupal6 data into JSON for Mirrors")
    parser.add_argument('component',
            choices=COMPONENT_TYPE_CHOICES,
            help="specify component to convert (or `all` for everything)")
    parser.add_argument(
            '-r', '--range',
            type=int, nargs=2,
            help="range of Drupal records to return by NID"
            )
    parser.add_argument('-n', '--number', type=int, help="number of Drupal records to return")
    parser.add_argument(
            '-o', '--offset',
            type=int, default=0,
            help="offset for the number of returned records")
    parser.add_argument('-v', '--verbosity', action="count", default=0)
    args = parser.parse_args()

    if args.verbosity >= 3:
        loglevel = logging.DEBUG
    elif args.verbosity == 2:
        loglevel = logging.INFO
    else:
        loglevel = logging.NOTSET
    logging.root.setLevel(level=loglevel)

    bounds = [args.offset, args.number]

    if args.component == 'debug':
        debug()
    else:
        build_component(args.component, bounds, args.range)

if __name__ == '__main__':
    main()
