from aztk_aci import models
from .operations import deploy, delete, get, diagnostics


class ClusterOperations():

    def create(self, cluster_configuration: models.ClusterConfiguration):
        deploy.deploy(cluster_configuration)

    def get(self, id: str):
        get.get(id)

    def delete(self, id: str):
        delete.delete(id)

    def diagnositcs(self, id: str):
        diagnostics.diagnostic(id)