import os
from aztk_aci_cli import constants
from aztk_aci import models
import yaml


def read_cluster_configuration(**kwargs):
    path = kwargs.get('config_path')
    if not path:
        path = constants.DEFAULT_CLUSTER_CONFIGURATION_PATH

    with open(path) as stream:
        cluster_configuration_dict = yaml.load(stream)
    return models.ClusterConfiguration().from_dict(cluster_configuration_dict)


def merge_cluster_configuration(cluster_configuration_args_dict: dict):
    ''' Merge CLI args with cluster.yaml

    Arguments:
        id
        master_cpu
        master_memory_gb
        worker_count
        worker_cpu
        worker_memory_gb
    '''
    id = cluster_configuration_args_dict.get('id')
    master_cpu = cluster_configuration_args_dict.get('master-cpu')
    master_memory_gb = cluster_configuration_args_dict.get('master-memory-gb')
    worker_count = cluster_configuration_args_dict.get('worker-count')
    worker_cpu = cluster_configuration_args_dict.get('worker-cpu')
    worker_memory_gb = cluster_configuration_args_dict.get('worker-memory-gb')
