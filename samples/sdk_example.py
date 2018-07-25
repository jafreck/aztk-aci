from aztk_aci import Client
from aztk_aci import models

# Define secrets
secrets = models.Secrets(
    service_principal="",
    subscription_id="",
    storage_account_resource_id="",
)

# Instantiate a Client
client = Client(secrets)

# Define a cluster
cluster_configuration = models.ClusterConfiguration(
    id="test",
    master_resources=models.NodeResources(cpu=1, memory_gb=2),
    worker_count=5,
    worker_resources=models.NodeResources(cpu=1, memory_gb=2))

# create the cluster
client.cluster.create(cluster_configuration)

# get the cluster
client.cluster.get(id=cluster_configuration.id)

# delete the cluster
client.cluster.delete(id=cluster_configuration.id)
