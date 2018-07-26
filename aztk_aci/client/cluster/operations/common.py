from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.resource.resources.resource_management_client import \
    ResourceManagementClient
from msrestazure.azure_active_directory import ServicePrincipalCredentials
from azure.mgmt.storage import StorageManagementClient
from azure.cosmosdb.table.tableservice import TableService

from aztk_aci.models import Secrets
from aztk_aci import constants


def create_service_principal_credentials(secrets: Secrets):
    return ServicePrincipalCredentials(
        client_id=secrets.service_principal.client_id,
        secret=secrets.service_principal.credential,
        tenant=secrets.service_principal.tenant_id)


def create_aci_client(secrets: Secrets):
    credentials = create_service_principal_credentials(secrets)
    return ContainerInstanceManagementClient(
        credentials,
        secrets.subscription_id,
        base_url=None,
    )


def create_resource_management_client(secrets: Secrets):
    credentials = create_service_principal_credentials(secrets)
    return ResourceManagementClient(credentials, secrets.subscription_id)


def create_storage_table_service(secrets: Secrets):
    credentials = create_service_principal_credentials(secrets)
    match = constants.RESOURCE_ID_PATTERN.match(secrets.storage_account_resource_id)
    accountname = match.group('account')
    subscription = match.group('subscription')
    resourcegroup = match.group('resourcegroup')
    mgmt_client = StorageManagementClient(credentials, subscription)
    key = mgmt_client.storage_accounts.list_keys(resource_group_name=resourcegroup, account_name=accountname).keys[0].value
    # storage_client = CloudStorageAccount(accountname, key)
    # blob_client = storage_client.create_block_blob_service()
    table_service = TableService(account_name=accountname, account_key=key)

    return table_service
