import yaml
from aztk_aci import models


def read_secrets(secrets_file: str):
    with open(secrets_file) as stream:
        secrets_dict = yaml.load(stream)
    return models.Secrets().from_dict(secrets_dict)
