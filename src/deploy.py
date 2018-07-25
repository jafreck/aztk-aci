import concurrent.futures

import azure.mgmt.containerinstance
import yaml
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tableservice import TableService
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (Container, ContainerGroup, ContainerGroupNetworkProtocol,
                                                 ContainerGroupRestartPolicy, ContainerPort, EnvironmentVariable, IpAddress,
                                                 OperatingSystemTypes, Port, ResourceRequests, ResourceRequirements)
from azure.mgmt.resource.resources.models import (ResourceGroup, ResourceGroupProperties)
from azure.mgmt.resource.resources.resource_management_client import \
    ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.common import CloudStorageAccount
from msrestazure.azure_active_directory import ServicePrincipalCredentials

import constants
import error
from logger import log
from models import Secrets


def create_container_group_multi(**kwargs):
    """Creates a container group with two containers in the specified
       resource group.

    Arguments:
        aci_client {azure.mgmt.containerinstance.ContainerInstanceManagementClient}
                    -- An authenticated container instance management client.
        resource_group {azure.mgmt.resource.resources.models.ResourceGroup}
                    -- The resource group in which to create the container group.
        container_group_name {str}
                    -- The name of the container group to create.
        containers {List[azure.mgmt.containerinstance.models.Container]}
        container_group_ports {List[azure.mgmt.containerinstance.models.Port]}
    """
    aci_client = kwargs.get('aci_client')
    resource_group = kwargs.get('resource_group')
    container_group_name = kwargs.get('container_group_name')
    containers = kwargs.get('containers')

    log.info("Creating container group '{0}'...".format(container_group_name))

    # Configure the container group
    ports = []
    for container_group_port in kwargs.get('container_group_ports'):
        ports.append(container_group_port)

    group_ip_address = IpAddress(ports=ports, dns_name_label=container_group_name)
    group = ContainerGroup(
        location=resource_group.location,
        containers=containers,
        os_type=OperatingSystemTypes.linux,
        ip_address=group_ip_address,
        restart_policy=ContainerGroupRestartPolicy.never)

    # Create the container group
    aci_client.container_groups.create_or_update(resource_group.name, container_group_name, group)

    # Get the created container group
    container_group = aci_client.container_groups.get(resource_group.name, container_group_name)

    log.info("Once DNS has propagated, container group '{0}' will be reachable at"
             " http://{1}".format(container_group_name, container_group.ip_address.fqdn))

    return container_group


def create_container(*args, **kwargs):
    return Container(
        name=kwargs.get('container_name'),
        image=kwargs.get('image'),
        resources=kwargs.get('resources'),
        command=kwargs.get('command'),
        ports=kwargs.get('ports'),
        environment_variables=kwargs.get('environment_variables'),
        volume_mounts=kwargs.get('volume_mounts'))


def create_spark_master_container(*args, **kwargs):
    container_resource_requests = ResourceRequests(memory_in_gb=2, cpu=1.0)
    container_resource_requirements = ResourceRequirements(requests=container_resource_requests)
    # command = ["/bin/bash", "-c", "\"/usr/bin/supervisorctl start master\""]  #TODO
    return create_container(
        container_name=kwargs.get('cluster_id') + '-master',
        image=kwargs.get('image') + "-master",
        resources=container_resource_requirements,
        # command=command,
        ports=[
            ContainerPort(port=8080, protocol='TCP'),
            ContainerPort(port=7077, protocol='TCP'),
        ],
        environment_variables=kwargs.get('environment_variables'),
        volume_mounts=kwargs.get('volume_mounts'))


def create_spark_worker_container(*args, **kwargs):
    container_resource_requests = ResourceRequests(memory_in_gb=2, cpu=1.0)
    container_resource_requirements = ResourceRequirements(requests=container_resource_requests)
    # command = ["worker {}".format(kwargs.get('master_ip'))]  #TODO
    container_name = kwargs.get('cluster_id') + '-worker-' + str(kwargs.get("worker_number"))
    return create_container(
        container_name=container_name,
        image=kwargs.get('image') + "-worker",
        resources=container_resource_requirements,
        # command=command,
        environment_variables=[EnvironmentVariable(name="MASTER_IP", value=kwargs.get('master_ip'))],
        ports=[
            ContainerPort(port=7077, protocol='TCP'),
            ContainerPort(port=4040, protocol='TCP'),
        ],
        volume_mounts=kwargs.get('volume_mounts'))


def create_extension_container(*args, **kwargs):
    container_resource_requests = ResourceRequests(memory_in_gb=2, cpu=1.0)
    container_resource_requirements = ResourceRequirements(requests=container_resource_requests)
    command = [],  #TODO
    return create_container(
        container_name=kwargs.get('cluster_id') + '-extension-server',
        image=kwargs.get('image'),
        resources=container_resource_requirements,
        command=command,
        ports=[],  #TODO
        environment_variables=kwargs.get('environment_variables'),
        volume_mounts=kwargs.get('volume_mounts'))


def create_cluster_storage_table(*args, **kwargs):
    table_service = kwargs.get('storage_table_service')
    # TODO: try-except
    success = table_service.create_table(kwargs.get('cluster_id'))

    # if not success:
    #     raise error.AztkError("Storage Table with same name already exists. Please delete the cluster {}".format(kwargs.get('cluster_id')))


def insert_entity_to_table(storage_table_service, table_name, entity):
    log.info("inserting:", entity, "to", table_name)
    storage_table_service.insert_entity(table_name, entity)


def update_storage_cluster_table(**kwargs):
    import uuid
    storage_table_service = kwargs.get('storage_table_service')
    cluster_id = kwargs.get('cluster_id')
    container_groups = kwargs.get('container_groups')

    entities = []
    for container_group in container_groups:
        entity = Entity()
        entity.PartitionKey = 'id'
        entity.RowKey = str(uuid.uuid4())
        entity.id = container_group.name
        entity.ip = container_group.ip_address.ip
        entities.append(entity)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(insert_entity_to_table, storage_table_service, cluster_id, entity): entity for entity in entities
        }
    concurrent.futures.wait(futures, timeout=30, return_when=concurrent.futures.ALL_COMPLETED)


def create_spark_cluster(*args, **kwargs):
    # create storage table and resource group to hold aci instances
    create_cluster_storage_table(
        storage_table_service=kwargs.get('storage_table_service'),
        cluster_id=kwargs.get('cluster_id'),
    )
    resource_group = get_resource_group(
        resource_management_client=kwargs.get('resource_management_client'),
        resource_group_name=kwargs.get('resource_group_name'),
    )

    # define master container
    master_container = create_spark_master_container(cluster_id=kwargs.get('cluster_id'), image=kwargs.get('image'))

    # create master container group
    master_container_group = create_container_group_multi(
        aci_client=kwargs.get('aci_client'),
        resource_group=resource_group,
        container_group_name=kwargs.get('cluster_id'),
        containers=[master_container],
        container_group_ports=[
            Port(protocol=ContainerGroupNetworkProtocol.tcp, port=8080),
            Port(protocol=ContainerGroupNetworkProtocol.tcp, port=7077),
        ])

    while master_container_group.ip_address.ip is None:
        master_container_group = kwargs.get('aci_client').container_groups.get(
            kwargs.get('resource_group_name'), kwargs.get('cluster_id'))

    # define worker containers
    worker_containers = [
        create_spark_worker_container(
            cluster_id=kwargs.get('cluster_id'),
            image=kwargs.get('image'),
            worker_number=i,
            master_ip=master_container_group.ip_address.ip,
        ) for i in range(kwargs.get("worker_count"))
    ]

    # create worker container groups
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(
                create_container_group_multi,
                aci_client=kwargs.get('aci_client'),
                resource_group=resource_group,
                container_group_name=container.name,
                containers=[container],
                container_group_ports=[
                    Port(protocol=ContainerGroupNetworkProtocol.tcp, port=7077),
                ],
            ): container for container in worker_containers
        }
        done_futures, not_done_futures = concurrent.futures.wait(
            futures, timeout=30, return_when=concurrent.futures.ALL_COMPLETED)
        #TODO: handle errors if future is not of type azure.mgmt.containerinstance.models.ContainerGroup

        worker_container_groups = [future.result() for future in done_futures]

    update_storage_cluster_table(
        storage_table_service=kwargs.get('storage_table_service'),
        cluster_id=kwargs.get('cluster_id'),
        container_groups=[master_container_group] + worker_container_groups,
    )
    return [master_container_group] + worker_container_groups


def get_resource_group(**kwargs):
    """ Get or create a Resource Group
    
    Arguments:
        resource_management_client
        resource_group_name
        location

    """
    resource_management_client = kwargs.get('resource_management_client')
    resource_group_name = kwargs.get('resource_group_name')
    location = kwargs.get('location')

    if resource_management_client.resource_groups.check_existence(resource_group_name):
        return resource_management_client.resource_groups.get(resource_group_name)
    else:
        return resource_management_client.resource_groups.create_or_update(resource_group_name=resource_group_name)


def create_service_principal_credentials(secrets):
    return ServicePrincipalCredentials(
        client_id=secrets.service_principal.client_id,
        secret=secrets.service_principal.credential,
        tenant=secrets.service_principal.tenant_id)


def create_aci_client(secrets):
    credentials = create_service_principal_credentials(secrets)
    return ContainerInstanceManagementClient(
        credentials,
        secrets.subscription_id,
        base_url=None,
    )


def create_resource_management_client(secrets):
    credentials = create_service_principal_credentials(secrets)
    return ResourceManagementClient(credentials, secrets.subscription_id)


def create_storage_table_service(secrets):
    credentials = create_service_principal_credentials(secrets)
    match = constants.RESOURCE_ID_PATTERN.match(secrets.storage_account_resource_id)
    accountname = match.group('account')
    subscription = match.group('subscription')
    resourcegroup = match.group('resourcegroup')
    mgmt_client = StorageManagementClient(credentials, subscription)
    key = mgmt_client.storage_accounts.list_keys(resource_group_name=resourcegroup, account_name=accountname).keys[0].value
    # storage_client = CloudStorageAccount(accountname, key)
    # blob_client = storage_client.create_block_blob_service()
    table_service = TableService(account_name=accountname, account_key=key)

    return table_service


def read_secrets(secrets_file):
    with open(secrets_file) as stream:
        secrets_dict = yaml.load(stream)
    return Secrets().from_dict(secrets_dict)


if __name__ == "__main__":
    import os
    import sys
    secrets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "secrets.yaml")
    secrets = read_secrets(secrets_path)
    aci_client = create_aci_client(secrets)

    resource_management_client = create_resource_management_client(secrets)

    storage_table_service = create_storage_table_service(secrets)

    container_groups = create_spark_cluster(
        worker_count=5,
        resource_management_client=resource_management_client,
        storage_table_service=storage_table_service,
        image="aztk/staging:spark-aci",
        aci_client=aci_client,
        resource_group_name="spark-aci",
        cluster_id="testsparkcluster" + sys.argv[1])
