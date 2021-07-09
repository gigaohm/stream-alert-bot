import sys
import yaml

DEFAULT_SETTINGS_PATH = "etc/settings.yml"


def load_yaml_settings():
    with open(DEFAULT_SETTINGS_PATH, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as yaml_exc:
            print(yaml_exc)
            sys.exit(1)
