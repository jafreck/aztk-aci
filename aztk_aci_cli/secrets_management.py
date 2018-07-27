import yaml
from aztk_aci import models
from aztk_aci_cli import constants


def read_secrets(secrets_file: str):
    if not secrets_file:
        secrets_file = constants.DEFAULT_SECRETS_CONFIGURATION_PATH
    with open(secrets_file) as stream:
        secrets_dict = yaml.load(stream)
    return models.Secrets().from_dict(secrets_dict)
