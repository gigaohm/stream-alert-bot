from logging import getLogger

from sab import constants
from sab.api.consumers import TrovoConsumer, TwitchConsumer


logger = getLogger("stream-alert-bot/api/consumer")
consumers_reference = {
    "twitch": TwitchConsumer,
    "trovo": TrovoConsumer
}


def create_consumer(consumer_type: str,
                    credentials: dict) -> constants.consumer_types:
    return consumers_reference[consumer_type](credentials)
