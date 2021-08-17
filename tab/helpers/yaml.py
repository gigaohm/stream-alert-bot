import sys
import yaml
import os.path


# TODO: Add logging
def load_yaml(file_path):
    try:
        with open(file_path, 'r') as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as yaml_e:
        print(yaml_e)
        sys.exit(1)
    except FileNotFoundError as fnf_e:
        print(fnf_e)
        sys.exit(1)
