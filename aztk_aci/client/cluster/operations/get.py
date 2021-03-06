from .common import create_aci_client, create_resource_management_client, create_storage_table_service
from aztk_aci import models


def print_cluster(**kwargs):
    '''
    Arguments:
        entities (:obj:`azure.cosmosdb.table.models.Entity`): Table entites representing nodes to print
    '''
    # TODO: move this to cli
    entities = kwargs.get('entities')
    cluster_id = kwargs.get('cluster_id')
    unerline_print_format = '-' * 65
    cluster_title_format = '| {:<62}|'
    title_print_format = '| {:^40}| {:^20}|'
    entry_print_format = '| {:<40}| {:<20}|'

    # cpus = 0
    # memory_in_gb = 0
    # for entity in entities:
    #     cpus += int(entity.cpus)
    #     memory_in_gb += int(entity.memory_in_gb)

    # total_cost = (0.000005 * memory_in_gb) + (0.000014 * cpus)

    # print("COST: Memory: $0.000005 * {} + $0.000014 * {} = {}".format(memory_in_gb, cpus, total_cost))

    print(unerline_print_format)
    print(cluster_title_format.format("Cluster: " + cluster_id))
    print(unerline_print_format)
    print(title_print_format.format("ID", "IP Address"))
    print(unerline_print_format)
    for entity in entities:
        print(entry_print_format.format(entity.id, entity.ip))
    print(unerline_print_format)


def list_clusters(**kwargs):
    """ List clusters

    __Note__: this assumes that Storage Tables are only used for clusters
    """
    pass


def get_cluster(**kwargs):
    """ Get the storage table related to the cluster

    Arguments:
        table_service
        cluster_id
    """

    table_service = kwargs.get('table_service')
    cluster_id = kwargs.get('cluster_id')
    table_entities = table_service.query_entities(table_name=cluster_id, filter="PartitionKey eq 'id'")
    entities = [e for e in table_entities]
    print_cluster(cluster_id=cluster_id, entities=entities)


def get(secrets: models.Secrets, id: str):
    # TODO: this should return a cluster object, not print
    storage_table_service = create_storage_table_service(secrets)

    get_cluster(table_service=storage_table_service, cluster_id=id)


# if __name__ == "__main__":
#     import os
#     import sys
#     secrets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "secrets.yaml")
#     secrets = deploy.read_secrets(secrets_path)
#     storage_table_service = deploy.create_storage_table_service(secrets)

#     cluster_id = sys.argv[1]

#
