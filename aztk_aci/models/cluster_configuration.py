from .node_resources import NodeResources


class ClusterConfiguration:

    def __init__(self, **kwargs):
        """
        Arguments:
            id(:obj:`str`): the unqiue id for the cluster
            master_resources(:obj:`models.NodeResources`): the resources to allocate for the master node
            worker_resources(:obj:`models.NodeResources`): the resources to allocate for each worker ndoe
            worker_count(:obj:`int`): the number of workers

        """
        self.id = kwargs.get('id')
        self.master_resources = kwargs.get("master_resources")
        self.worker_count = kwargs.get('worker_count')
        self.worker_resources = kwargs.get('worker_resources')

    def from_dict(self, cluster_configuration_dict):
        self.id = cluster_configuration_dict['id']
        master_resources_dict = cluster_configuration_dict['master_resources']
        self.master_resources = NodeResources().from_dict(master_resources_dict)
        self.worker_count = cluster_configuration_dict['worker_count']
        worker_resources_dict = cluster_configuration_dict['worker_resources']
        self.worker_resources = NodeResources().from_dict(worker_resources_dict)

        return self
