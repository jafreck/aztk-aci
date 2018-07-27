class NodeResources:

    def __init__(self, cpu: int = None, memory_gb: int = None):
        self.cpu = cpu
        self.memory_gb = memory_gb

    def from_dict(self, node_resources_dict):
        self.cpu = node_resources_dict['cpu']
        self.memory_gb = node_resources_dict['memory_gb']

        return self