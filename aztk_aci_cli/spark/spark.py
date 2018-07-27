import argparse
import typing

from .cluster import cluster


def setup_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(title="Actions", dest="action", metavar="<action>")
    subparsers.required = True

    cluster_parser = subparsers.add_parser("cluster", help="Commands to manage a cluster")
    job_parser = subparsers.add_parser("job", help="Commands to manage a Job")
    init_parser = subparsers.add_parser("init", help="Initialize your environment")

    cluster.setup_parser(cluster_parser)


def execute(args: typing.NamedTuple):
    actions = dict(cluster=cluster.execute)
    func = actions[args.action]
    func(args)
