#!/usr/bin/env python
from components.base import build_component
import argparse
import logging
import local_settings as settings


def main():
    COMPONENT_TYPE_CHOICES = ['article', 'all']
    parser = argparse.ArgumentParser(
            description="Converts Drupal6 data into JSON for Mirrors")
    parser.add_argument('component', choices=COMPONENT_TYPE_CHOICES, help="specify component to convert (or `all` for everything)")
    parser.add_argument('-n', '--number', type=int, help="number of Drupal records to return")
    parser.add_argument('-v', '--verbosity', action="count", default=0)
    args = parser.parse_args()
    if args.verbosity >= 3:
        loglevel = logging.DEBUG
    elif args.verbosity == 2:
        loglevel = logging.INFO
    else:
        loglevel = logging.NOTSET
    logging.basicConfig(level=loglevel)
    build_component(args.component, args.number)

if __name__ == '__main__':
    main()
