from azure.mgmt.containerinstance.models import ContainerExecRequestTerminalSize
from aztk_aci import models
from .common import create_aci_client, create_resource_management_client, create_storage_table_service


def diagnostic(secrets: models.Secrets, id: str):
    pass


# if __name__ == "__main__":
#     import deploy
#     import os
#     import sys
#     secrets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "secrets.yaml")
#     secrets = deploy.read_secrets(secrets_path)
#     aci_client = deploy.create_aci_client(secrets)

#     container_group_name = sys.argv[1]
#     print(aci_client.container.list_logs("spark-aci", container_group_name, container_group_name + "-master"))

#     result = aci_client.container.execute_command(
#         "spark-aci",
#         container_group_name,
#         container_group_name + "-master",
#         command=sys.argv[2],
#         terminal_size=ContainerExecRequestTerminalSize(rows=100, cols=120),
#     )
#     print(result)

#     cg = aci_client.container_groups.get("spark-aci", container_group_name)
#     master_container = cg.containers[0]
#     print(master_container.instance_view.events[-1].message)
