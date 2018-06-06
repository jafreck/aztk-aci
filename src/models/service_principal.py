class ServicePrincipal:
    def __init__(self):
        self.client_id = None
        self.tenant_id = None
        self.credential = None
    
    def from_dict(self, service_principal_dict):
        self.client_id = service_principal_dict['client_id']
        self.tenant_id = service_principal_dict['tenant_id']
        self.credential = service_principal_dict['credential']
        return self
        