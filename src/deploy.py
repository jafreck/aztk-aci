

import azure.mgmt.containerinstance
from azure.mgmt.containerinstance.models import(
    ContainerGroup,
    Container,
    ContainerInstanceManagementClient
)


aci_client = ContainerInstanceManagementClient(credentials, subscription_id, base_url=None)


def create_container_group(aci_client, resource_group,
                           container_group_name, container_image_name):
    """Creates a container group with a single container.

    Arguments:
        aci_client {azure.mgmt.containerinstance.ContainerInstanceManagementClient}
                    -- An authenticated container instance management client.
        resource_group {azure.mgmt.resource.resources.models.ResourceGroup}
                    -- The resource group in which to create the container group.
        container_group_name {str}
                    -- The name of the container group to create.
        container_image_name {str}
                    -- The container image name and tag, for example:
                       microsoft\aci-helloworld:latest
    """
    print("Creating container group '{0}'...".format(container_group_name))

    # Configure the container
    container_resource_requests = ResourceRequests(memory_in_gb=1, cpu=1.0)
    container_resource_requirements = ResourceRequirements(
                                        requests=container_resource_requests)
    container = Container(name=container_group_name,
                          image=container_image_name,
                          resources=container_resource_requirements,
                          ports=[ContainerPort(port=80)])

    # Configure the container group
    ports = [Port(protocol=ContainerGroupNetworkProtocol.tcp, port=80)]
    group_ip_address = IpAddress(ports=ports,
                                 dns_name_label=container_group_name)
    group = ContainerGroup(location=resource_group.location,
                           containers=[container],
                           os_type=OperatingSystemTypes.linux,
                           ip_address=group_ip_address)

    # Create the container group
    aci_client.container_groups.create_or_update(resource_group.name,
                                                 container_group_name,
                                                 group)

    # Get the created container group
    container_group = aci_client.container_groups.get(resource_group.name,
                                                      container_group_name)

    print("Once DNS has propagated, container group '{0}' will be reachable at"
          " http://{1}".format(container_group_name,
                               container_group.ip_address.fqdn))



def create_container(*args, **kwargs):
    return Container(name, image, resources, command=None, ports=None, environment_variables=None, volume_mounts=None)


def create_master_container(*args, **kwargs):
    return create_container(name, image, resources, command=None, ports=None, environment_variables=None, volume_mounts=None)


def create_worker_container(*args, **kwargs):
    return create_container(name, image, resources, command=None, ports=None, environment_variables=None, volume_mounts=None)


def create_extension_container(*args, **kwargs):
    return create_container(name, image, resources, command=None, ports=None, environment_variables=None, volume_mounts=None)


def create_spark_cluster(*args, **kwargs)
    master_container = create_master_container()


def create_aci_client(secrets):
    return ContainerInstanceManagementClient(credentials, subscription_id, base_url=None)

def create_