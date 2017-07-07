#!/usr/bin/env python

from __future__ import print_function
import os
import argparse
import sys

from storystats.utils import print_bugs, print_story_stats

def validate_args(args):
    if not args.token or not args.project_id or not args.url:
        print('All url, token and project_id arguments must be provided!',
              file=sys.stderr)
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser('Tool to get file stats'
                                     ' for stories from PivotalTracker')
    parser.add_argument('-u', '--url', dest='url', type=str,
                        default=os.environ.get('TRACKER_URL', None),
                        help='PivotalTracker url with services/v5 extension')
    parser.add_argument('-p', '--project-id', dest='project_id', type=str,
                        default=os.environ.get('TRACKER_PROJECT_ID', None),
                        help='TrackerTracker target project')
    parser.add_argument('-t', '--token', dest='token', type=str,
                        default=os.environ.get('TRACKER_TOKEN', None),
                        help='PivotalTracker token used for authentication')
    parser.add_argument('-r', '--repos-path', dest='repos_path', type=str,
                        default=os.environ.get('GIT_REPOS_PATH', None),
                        help='Path to where to download/use the repos')

    parser.add_argument('-l', '--list-bugs', action='store_true', dest='list',
                        help='List accepted bugs in the given project')
    parser.add_argument('-s', '--stat', dest='story_id', type=str, default=None,
                        help='Print file stats for the given story id')
    return parser.parse_args()

def main():
    args = parse_args()
    validate_args(args)

    if args.list:
        print_bugs(args)
    elif args.story_id:
        if not args.repos_path or not os.path.isdir(args.repos_path):
            print('repos path arguments is required for --stat',
                  file=sys.stderr)
            sys.exit(1)
        print_story_stats(args)
    else:
        print('No action')

if __name__ == '__main__':
    main()
