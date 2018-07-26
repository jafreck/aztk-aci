from aztk_aci import models
from .operations import deploy, delete, get, diagnostics


class ClusterOperations():

    def __init__(self, secrets: models.Secrets):
        self._secrets = secrets

    def create(self, cluster_configuration: models.ClusterConfiguration):
        deploy.deploy(self._secrets, cluster_configuration)

    def get(self, id: str):
        get.get(self._secrets, id)

    def delete(self, id: str):
        delete.delete(self._secrets, id)

    def diagnositcs(self, id: str):
        diagnostics.diagnostic(self._secrets, id)
