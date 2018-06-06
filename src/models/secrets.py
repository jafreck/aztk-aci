from .service_principal import ServicePrincipal

class Secrets:
    def __init__(self):
        self.service_principal = None
        self.subscription_id = None

    def from_dict(self, secrets_dict):
        service_principal_dict = secrets_dict['service_principal']
        self.service_principal = ServicePrincipal().from_dict(service_principal_dict)
        self.subscription_id = secrets_dict['subscription_id']
        return self