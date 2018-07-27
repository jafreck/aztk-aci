import argparse

from aztk_aci import Client, models
from aztk_aci_cli import secrets_management


def setup_parser(parser: argparse.ArgumentParser):
    parser.add_argument('--id', type=str, help='The unique id of your spark cluster')
    parser.add_argument('--master-cpu', type=int, help='Number of vCPUs for your master node.')
    parser.add_argument('--master-memory-gb', type=int, help='Number of memory (GBs) for your master node.')
    parser.add_argument('--worker-count', type=int, help='Number of workers in your cluster')
    parser.add_argument('--worker-cpu', type=int, help='Number of vCPUs for each of your worker nodes.')
    parser.add_argument('--worker-memory-gb', type=int, help='Number of memory (GBs) for each of your worker nodes.')
    parser.add_argument('--secrets-path', type=str, help='Path to your secrets.yaml configuration file.')


def execute(args):
    secrets = secrets_management.read_secrets(vars(args).get('secrets_file'))

    # Instantiate a Client
    client = Client(secrets)

    # Define a cluster
    # TODO: add merge with config file
    cluster_configuration = models.ClusterConfiguration(
        id=args.id,
        master_resources=models.NodeResources(cpu=args.master_cpu, memory_gb=args.master_memory_gb),
        worker_count=args.worker_count,
        worker_resources=models.NodeResources(cpu=args.master_cpu, memory_gb=args.master_memory_gb))

    # create a cluster
    cluster = client.cluster.create(cluster_configuration)

    print_format = "Spark Master UI: http://{}:8080"
    for container_group in cluster:
        if container_group.name == args.id:
            print(print_format.format(container_group.ip_address.fqdn))
            test_availability("http://{}:8080".format(container_group.ip_address.fqdn))


def test_availability(url: str):
    import requests

    while True:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
