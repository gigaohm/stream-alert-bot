from logging import getLogger
import os.path
import sys
import yaml


logger = getLogger("stream-alert-bot/helper/yaml")


def load_yaml(file_path):
    try:
        logger.debug(" ".join(["Opening settings file at", file_path]))
        with open(file_path, "r") as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as yaml_e:
        logger.error("Provided file could not be parsed as a YAML file.")
        sys.exit(5)
    except FileNotFoundError as fnf_e:
        logger.error("Provided file path does not exist.")
        sys.exit(2)
