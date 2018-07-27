import argparse
import typing

from .endpoints import create, delete, get


class ClusterAction:
    create = "create"
    delete = "delete"
    get = "get"


def setup_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(title="Actions", dest="cluster_action", metavar="<action>")
    subparsers.required = True

    create_parser = subparsers.add_parser(ClusterAction.create, help="Create a new cluster")
    delete_parser = subparsers.add_parser(ClusterAction.delete, help="Delete a cluster")
    get_parser = subparsers.add_parser(ClusterAction.get, help="Get information about a cluster")

    create.setup_parser(create_parser)
    delete.setup_parser(delete_parser)
    get.setup_parser(get_parser)


def execute(args: typing.NamedTuple):
    actions = {}

    actions[ClusterAction.create] = create.execute
    actions[ClusterAction.delete] = delete.execute
    actions[ClusterAction.get] = get.execute

    func = actions[args.cluster_action]
    func(args)
