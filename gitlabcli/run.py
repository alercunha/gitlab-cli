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


def pipelines(api: GitlabAPI, args):
    data = api.pipelines(args.project, args.id, args.ref)
    print_json(data)


def pipeline_jobs(api: GitlabAPI, args):
    data = api.pipeline_jobs(args.project, args.id)
    return print_json(data)


def main():
    parser = argparse.ArgumentParser(description='Access gitlab API')

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    common_parser.add_argument('-t', '--token', help='Private token to call the API')

    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('commits', help='Get commits from a repository', parents=[common_parser])
    subparser.add_argument('project', help='The project id or path (i.e. 1 or namespace/project)')
    subparser.add_argument('-r', '--ref_name', help='The name of a repository branch or tag or if not given the default branch')
    subparser.add_argument('-s', '--since', help='Only commits after or on this date will be returned in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ')
    subparser.add_argument('-u', '--until', help='Only commits before or on this date will be returned in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ')
    subparser.set_defaults(func=commits)

    subparser = subparsers.add_parser('tags', help='Get tags from a repository', parents=[common_parser])
    subparser.add_argument('project', help='The project id or path (i.e. 1 or namespace/project)')
    subparser.add_argument('-n', '--name', help='The name of the tag')
    subparser.set_defaults(func=tags)

    subparser = subparsers.add_parser('pipelines', help='Get pipelines of a project', parents=[common_parser])
    subparser.add_argument('project', help='The project id or path (i.e. 1 or namespace/project)')
    subparser.add_argument('--id', help='The ID of a specific pipeline')
    subparser.add_argument('-r', '--ref', help='The ref of pipelines')
    subparser.set_defaults(func=pipelines)

    subparser = subparsers.add_parser('pipeline_jobs', help='Get pipeline jobs of a project', parents=[common_parser])
    subparser.add_argument('project', help='The project id or path (i.e. 1 or namespace/project)')
    subparser.add_argument('id', help='The ID of a pipeline')
    subparser.set_defaults(func=pipeline_jobs)

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
