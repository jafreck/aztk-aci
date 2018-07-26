from .service_principal import ServicePrincipal


class Secrets:

    def __init__(self, service_principal=None, subscription_id=None, storage_account_resource_id=None):
        self.service_principal = service_principal
        self.subscription_id = subscription_id
        self.storage_account_resource_id = storage_account_resource_id

    def from_dict(self, secrets_dict):
        service_principal_dict = secrets_dict['service_principal']
        self.service_principal = ServicePrincipal().from_dict(service_principal_dict)
        self.subscription_id = secrets_dict['subscription_id']
        self.storage_account_resource_id = secrets_dict['storage_account_resource_id']
        return self
