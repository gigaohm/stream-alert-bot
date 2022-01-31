from logging import getLogger

from sab import constants
from sab.api.publishers import TwitterPublisher


logger = getLogger("stream-alert-bot/api/publisher")
publishers_reference = {"twitter": TwitterPublisher}


def create_publishers(publisher_dict: dict) -> constants.publisher_types:
    publishers = []
    for publisher, creds in publisher_dict.items():
        publishers += [publishers_reference[publisher](creds)]
    return publishers
