import argparse
import json

import requests

import logging


_api_url = 'https://gitlab.com/api/v4/{0}'


def _get(path, args, **kwg):
    headers = None
    if args.token:
        headers = {'PRIVATE-TOKEN': args.token}
    url = _api_url.format(path.lstrip('/'))
    params = {k: v for k, v in kwg.items() if v is not None}
    r = requests.get(url, headers=headers, params=params)
    if args.verbose:
        print('URL: {0}'.format(r.request.url))
    return r.json()


def repo_url(project):
    return '/projects/{0}/repository'.format(project.replace('/', '%2F'))


def commits(args):
    data = _get(repo_url(args.project) + '/commits', args, ref_name=args.ref_name, since=args.since, until=args.until)
    print(json.dumps(data, indent=2))


def tags(args):
    if args.tag_name:
        data = _get(repo_url(args.project) + '/tags/' + args.tag_name, args)
    else:
        data = _get(repo_url(args.project) + '/tags', args)
    print(json.dumps(data, indent=2))


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
    subparser.add_argument('--tag_name', help='The name of the tag')
    subparser.set_defaults(func=tags)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        logging.basicConfig(level=logging.INFO)
        args.func(args)
        exit(0)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
