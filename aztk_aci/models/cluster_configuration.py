class ClusterConfiguration():

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
