import concurrent.futures


def delete_cluster(**kwargs):
    """Delete a cluster

    Arguments:
        aci_client (`obj:azure.mgmt.containerinstance.ContainerInstanceManagementClient)
        cluster_id (`obj:str:`): id of the cluster to delete
        resource_group (`obj:str:`): id of the resource_group the cluster was created under
    """
    aci_client = kwargs.get('aci_client')
    cluster_id = kwargs.get('cluster_id')

    container_groups = [
        container_group for container_group in aci_client.container_groups.list() if cluster_id in container_group.name
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(aci_client.container_groups.delete, kwargs.get('resource_group'), container_group.name):
            container_group for container_group in container_groups
        }
        concurrent.futures.wait(futures, timeout=30, return_when=concurrent.futures.ALL_COMPLETED)

    # for container_group in container_groups:
    #     print("Found {}".format(container_group.name))
    #     print("cluster_id:", cluster_id)
    #     if cluster_id in container_group.name:
    #         print("{} in {}. Deleting".format(cluster_id, container_group.name))

    #         aci_client.container_groups.delete(kwargs.get('resource_group'), container_group.name)


if __name__ == "__main__":
    import deploy
    import os
    import sys
    secrets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "secrets.yaml")
    secrets = deploy.read_secrets(secrets_path)
    aci_client = deploy.create_aci_client(secrets)

    delete_cluster(
        aci_client=aci_client,
        resource_group=sys.argv[1],
        cluster_id=sys.argv[2],
    )
