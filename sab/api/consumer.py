from logging import getLogger
from trovoApi import TrovoClient
from twitchAPI.twitch import Twitch
from typing import Union

from sab.api.consumers import TrovoConsumer, TwitchConsumer


logger = getLogger("stream-alert-bot/api/consumer")


def create_consumer(consumer_type: str,
                    credentials: dict) -> Union[Twitch, TrovoClient]:
    consumersReference = {
        "twitch": TwitchConsumer,
        "trovo": TrovoConsumer
    }

    return consumersReference[consumer_type](credentials)
