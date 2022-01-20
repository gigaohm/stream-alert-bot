from logging import getLogger
from trovoApi import TrovoClient
from twitchAPI.twitch import Twitch
from typing import Union

from sab.api.consumers import TrovoConsumer, TwitchConsumer


logger = getLogger("stream-alert-bot/api/consumer")


def create_consumer(consumer_type: str,
                    credentials: dict) -> Union[Twitch, TrovoClient]:
    consumers_reference = {
        "twitch": TwitchConsumer,
        "trovo": TrovoConsumer
    }

    return consumers_reference[consumer_type](credentials)
