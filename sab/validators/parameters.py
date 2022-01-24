from typing import List
from logging import getLogger

from sab import constants

logger = getLogger("stream-alert-bot/validators/parameters")


def verify_consumer(consumer: str,
                    credentials: dict) -> dict:
    if consumer not in credentials:
        raise ValueError("".join(["Credentials for the provided consumer",
                                  " parameter (", consumer,
                                  ") are not present."]))
    logger.debug(" ".join(["Retrieved credentials for consumer",
                          consumer.capitalize()]))
    return credentials[consumer]


def verify_publishers(publishers_list: List[str],
                      credentials: dict) -> dict:
    pub_credentials = {}
    for publisher in publishers_list:
        if publisher not in credentials:
            raise ValueError("".join(["Credentials for the provided publisher",
                                      " parameter (", publisher,
                                      ") are not" " present."]))
        logger.debug(" ".join(["Retrieved credentials for publisher",
                              publisher.capitalize()]))
        pub_credentials[publisher] = credentials[publisher]
    return pub_credentials
