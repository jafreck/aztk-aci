import models
from cluster_operations import ClusterOperations


class Client():

    def __init__(self, secrets: models.Secrets):
        self.secrets = secrets
        self.cluster = ClusterOperations()
