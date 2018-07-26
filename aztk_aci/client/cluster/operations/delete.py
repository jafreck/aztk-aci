import concurrent.futures

from .common import create_aci_client, create_resource_management_client, create_storage_table_service
from aztk_aci.logger import log


def delete_container_group(aci_client, storage_table_service, resource_group, container_group_name):
    log.info("Deleting container group {} in resource group {}".format(container_group_name, resource_group))
    aci_client.container_groups.delete(resource_group, container_group_name)


def delete_cluster(**kwargs):
    """Delete a cluster

    Arguments:
        aci_client (:obj:`azure.mgmt.containerinstance.ContainerInstanceManagementClient)
        cluster_id (:obj:`str:`): id of the cluster to delete
        resource_group (:obj:`str:`): id of the resource_group the cluster was created under
        storage_table_service (:obj:`azure.mgmt.resource.resources.resource_management_client.ResourceManagementClient`): table service to delete cluster's storage table
    """
    aci_client = kwargs.get('aci_client')
    cluster_id = kwargs.get('cluster_id')
    resource_group = kwargs.get('resource_group')
    storage_table_service = kwargs.get('storage_table_service')

    container_groups = [
        container_group for container_group in aci_client.container_groups.list() if cluster_id in container_group.name
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(
                delete_container_group,
                aci_client,
                storage_table_service,
                resource_group,
                container_group.name,
            ): container_group for container_group in container_groups
        }
        concurrent.futures.wait(futures, timeout=30, return_when=concurrent.futures.ALL_COMPLETED)


def delete(secrets, id: str):
    aci_client = create_aci_client(secrets)
    storage_table_service = create_storage_table_service(secrets)
    delete_cluster(
        aci_client=aci_client,
        storage_table_service=storage_table_service,
        resource_group="spark-aci",  #TODO: create resource group for each cluster or otherwise get resource_group
        cluster_id=id,
    )


# if __name__ == "__main__":
#     import deploy
#     import os
#     import sys

#     secrets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "secrets.yaml")
#     secrets = deploy.read_secrets(secrets_path)
#     aci_client = deploy.create_aci_client(secrets)

#     delete_cluster(
#         aci_client=aci_client,
#         resource_group=sys.argv[1],
#         cluster_id=sys.argv[2],
#     )
