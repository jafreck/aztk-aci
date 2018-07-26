class ServicePrincipal:

    def __init__(self, client_id=None, tenant_id=None, credential=None):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.credential = credential

    def from_dict(self, service_principal_dict):
        self.client_id = service_principal_dict['client_id']
        self.tenant_id = service_principal_dict['tenant_id']
        self.credential = service_principal_dict['credential']
        return self
