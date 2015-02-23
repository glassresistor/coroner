#!/usr/bin/env python
from lib.base import rebuild_engine, build_articles
import argparse
import local_settings as settings

def build_component(component_type, number):
    if number:
        print("Limit them records")
    rebuild_engine()
    build_articles()

def main():
    COMPONENT_TYPE_CHOICES = ['article', 'all']
    parser = argparse.ArgumentParser(
            description="Converts Drupal6 data into JSON for Mirrors")
    parser.add_argument('component', choices=COMPONENT_TYPE_CHOICES, help="specify component to convert (or `all` for everything)")
    parser.add_argument('-n', '--number', type=int, help="number of Drupal records to return")
    args = parser.parse_args()
    build_component(args.component, args.number)

if __name__ == '__main__':
    main()
