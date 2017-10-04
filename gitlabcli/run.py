import argparse
import json

from gitlabcli.api import GitlabAPI

import logging


def print_json(result):
    print(json.dumps(result, indent=2))


def commits(api: GitlabAPI, args):
    data = api.commits(args.project, args.ref_name, args.since, args.until)
    print_json(data)


def tags(api: GitlabAPI, args):
    data = api.tags(args.project, args.name)
    print_json(data)


def main():
    parser = argparse.ArgumentParser(description='Access gitlab API')

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    common_parser.add_argument('-t', '--token', help='Private token to call the API')

    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('commits', help='Access commits from a repository', parents=[common_parser])
    subparser.add_argument('project', help='The project id or path (i.e. 1 or namespace/project)')
    subparser.add_argument('-r', '--ref_name', help='The name of a repository branch or tag or if not given the default branch')
    subparser.add_argument('-s', '--since', help='Only commits after or on this date will be returned in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ')
    subparser.add_argument('-u', '--until', help='Only commits before or on this date will be returned in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ')
    subparser.set_defaults(func=commits)

    subparser = subparsers.add_parser('tags', help='Access tags from a repository', parents=[common_parser])
    subparser.add_argument('project', help='The project id or path (i.e. 1 or namespace/project)')
    subparser.add_argument('-n', '--name', help='The name of the tag')
    subparser.set_defaults(func=tags)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        logging.basicConfig(level=logging.INFO)
        api = GitlabAPI(token=args.token, verbose=args.verbose)
        args.func(api, args)
        exit(0)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
