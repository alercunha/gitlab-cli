import argparse
import requests

import logging


_api_url = 'https://gitlab.com/api/v4/{0}'


def _get(path, args):
    headers = None
    if args.token:
        headers = {'PRIVATE-TOKEN': args.token}
    r = requests.get(_api_url.format(path.lstrip('/')), headers=headers)
    return r.json()


def commits(args):
    pass#print(_get('/


def tags(args):
    pass


def main():
    parser = argparse.ArgumentParser(description='Access gitlab API')
    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('commits', help='Access commits from a repository')
    subparser.add_argument('project_id', help='The project id or path (i.e. 1 or namespace/project)')
    subparser.add_argument('-t', '--token', help='Private token to call the API')
    subparser.add_argument('-r', '--ref_name', help='The name of a repository branch or tag or if not given the default branch')
    subparser.add_argument('-s', '--since', help='Only commits after or on this date will be returned in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ')
    subparser.add_argument('-u', '--until', help='Only commits before or on this date will be returned in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ')
    subparser.set_defaults(func=commits)

    subparser = subparsers.add_parser('tags', help='Access tags from a repository')
    subparser.add_argument('project', help='A project id (i.e. namespace/project)')
    #subparser.add_argument('-r', '--ref_name', help='The name of a repository branch or tag or if not given the default branch')
    #subparser.add_argument('-s', '--since', help='Only commits after or on this date will be returned in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ')
    #subparser.add_argument('-u', '--until', help='Only commits before or on this date will be returned in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ')
    subparser.set_defaults(func=tags)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        logging.basicConfig(level=logging.DEBUG)
        args.func(args)
        exit(0)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
