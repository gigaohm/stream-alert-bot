from logging import getLogger
from twitter import Api
from typing import List, Union

from sab.api.publishers import TwitterPublisher


logger = getLogger("stream-alert-bot/api/publisher")


def create_publishers(publisher_dict: dict) -> List[Union[Api]]:
    publishers_reference = {
        "twitter": TwitterPublisher
    }
    publishers = []
    for publisher, creds in publisher_dict.items():
        publishers += [publishers_reference[publisher](creds)]
    return publishers
