import typing
from logging import getLogger

from sab import constants

logger = getLogger("stream-alert-bot/validators/parameters")


def verify_service(service_name: str,
                   credentials: dict,
                   service_type: str) -> dict:
    if service_name not in credentials:
        raise ValueError("".join(["Credentials for the provided ",
                                  service_type, " parameter (", service_name,
                                  ") are not" " present."]))
    logger.debug("".join(["Retrieved credentials for ",
                          service_name.capitalize()]))
    return credentials[service_name]
