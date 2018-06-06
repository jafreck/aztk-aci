import azure.mgmt.containerinstance
import yaml
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (Container, ContainerGroup, ContainerGroupNetworkProtocol, ContainerPort,
                                                 ContainerGroupRestartPolicy, EnvironmentVariable, IpAddress,
                                                 OperatingSystemTypes, Port, ResourceRequests, ResourceRequirements)
from azure.mgmt.resource.resources.models import (ResourceGroup, ResourceGroupProperties)
from azure.mgmt.resource.resources.resource_management_client import \
    ResourceManagementClient
from msrestazure.azure_active_directory import ServicePrincipalCredentials

from models import Secrets


def create_container_group_multi(aci_client, resource_group, container_group_name, containers):
    """Creates a container group with two containers in the specified
       resource group.

    Arguments:
        aci_client {azure.mgmt.containerinstance.ContainerInstanceManagementClient}
                    -- An authenticated container instance management client.
        resource_group {azure.mgmt.resource.resources.models.ResourceGroup}
                    -- The resource group in which to create the container group.
        container_group_name {str}
                    -- The name of the container group to create.
        containers {List[azure.mgmt.containerinstance.Container]}
    """
    print("Creating container group '{0}'...".format(container_group_name))

    # Configure the container group
    ports = [Port(protocol=ContainerGroupNetworkProtocol.tcp, port=8080)]
    group_ip_address = IpAddress(ports, dns_name_label=container_group_name)
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

    print("Once DNS has propagated, container group '{0}' will be reachable at"
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
    command = [],  #TODO
    return create_container(
        container_name=kwargs.get('cluster_id') + '-master',
        image=kwargs.get('image'),
        resources=container_resource_requirements,
        command=command,
        ports=[ContainerPort(port=8080, protocol='TCP')],  #TODO
        environment_variables=kwargs.get('environment_variables'),
        volume_mounts=kwargs.get('volume_mounts'))


def create_spark_worker_container(*args, **kwargs):
    container_resource_requests = ResourceRequests(memory_in_gb=2, cpu=1.0)
    container_resource_requirements = ResourceRequirements(requests=container_resource_requests)
    command = [],  #TODO
    container_name = kwargs.get('cluster_id') + '-worker-' + str(kwargs.get("worker_number"))
    return create_container(
        container_name=container_name,
        image=kwargs.get('image'),
        resources=container_resource_requirements,
        command=command,
        ports=[],  #TODO
        environment_variables=kwargs.get('environment_variables'),
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


def create_spark_cluster(*args, **kwargs):
    master_container = [create_spark_master_container(cluster_id=kwargs.get('cluster_id'), image=kwargs.get('image'))]
    worker_containers = [
        create_spark_worker_container(
            cluster_id=kwargs.get('cluster_id'),
            image=kwargs.get('image'),
            worker_number=i,
        ) for i in range(kwargs.get("worker_count"))
    ]

    resource_group = get_resource_group(kwargs.get('resource_management_client'), kwargs.get('resource_group_name'))

    cg = create_container_group_multi(
        aci_client=kwargs.get('aci_client'),
        resource_group=resource_group,
        container_group_name=kwargs.get('cluster_id'),
        containers=master_container + worker_containers,
    )
    return cg


#TODO: change to get_or_create_resource_group
def get_resource_group(resource_management_client, resource_group_name):
    if resource_management_client.resource_groups.check_existence(resource_group_name):
        return resource_management_client.resource_groups.get(resource_group_name)
    else:
        # TODO: create resource group
        pass


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


def read_secrets(secrets_file):
    with open(secrets_file) as stream:
        secrets_dict = yaml.load(stream)
    return Secrets().from_dict(secrets_dict)


if __name__ == "__main__":
    import os
    secrets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "secrets.yaml")
    secrets = read_secrets(secrets_path)
    print(secrets)
    aci_client = create_aci_client(secrets)
    resource_management_client = create_resource_management_client(secrets)

    cluster = create_spark_cluster(
        worker_count=2,
        resource_management_client=resource_management_client,
        image="aztk/spark:v0.1.0-spark2.3.0-base",
        aci_client=aci_client,
        resource_group_name="spark-aci",
        cluster_id="test-spark-cluster")
