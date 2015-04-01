#!/usr/bin/env python
from components.base import rebuild_engine, build_articles, debug
import local_settings as settings
import argparse
import logging

def build_component(component_type, number):
    rebuild_engine()
    build_articles(number)

def main():
    COMPONENT_TYPE_CHOICES = ['article', 'all', 'debug']
    parser = argparse.ArgumentParser(
            description="Converts Drupal6 data into JSON for Mirrors")
    parser.add_argument('component',
            choices=COMPONENT_TYPE_CHOICES,
            help="specify component to convert (or `all` for everything)")
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

    if args.component == 'debug':
        debug()
    else:
        build_component(args.component, args.number)

if __name__ == '__main__':
    main()
