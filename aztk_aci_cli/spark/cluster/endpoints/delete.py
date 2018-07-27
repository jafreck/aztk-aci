import argparse
import typing

from aztk_aci import Client, models
from aztk_aci_cli import secrets_management


def setup_parser(parser: argparse.ArgumentParser):
    parser.add_argument('--id', type=str, help='The unique id of your spark cluster')
    parser.add_argument('--secrets-path', type=str, help='Path to your secrets.yaml configuration file.')


def execute(args: typing.NamedTuple):
    secrets = secrets_management.read_secrets(vars(args).get('secrets_file'))

    # Instantiate a Client
    client = Client(secrets)

    client.cluster.delete(id=args.id)

    # TODO: add output of some kind...
