from logging import Logger, getLogger
import sys

from requests.exceptions import ConnectionError
from typing import List
from twitchAPI.twitch import Twitch
from twitchAPI.types import TwitchAuthorizationException


class TwitchConsumer:
    client: Twitch = None

    __logger: Logger

    def __init__(self, credentials: dict):
        try:
            client_id = credentials["client_id"]
            secret = credentials["secret"]
            twitch = Twitch(client_id, secret)
            twitch.authenticate_app([])
            self.__logger = getLogger("stream-alert-bot/api/consumers/twitch")
            self.__logger.debug("Connection to Twitch successful")
            self.client = twitch
        except TwitchAuthorizationException as ta_e:
            self.__logger.error(
                ("Issues connecting to Twitch with provided " "credentials.")
            )
            sys.exit(1)
        except ConnectionError as c_e:
            self.__logger.error(("Not able to connect to API. Verify your " "network."))
            sys.exit(1)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    def get_all_streamers_info(self, streamers: dict) -> dict:
        try:
            twitch_users = list(streamers.keys())
            self.__logger.debug("Obtaining streamers info")
            streamers_info = self.__get_users(twitch_users)
            self.__logger.debug("Obtained streamers info:")
            self.__logger.debug(streamers_info)
            return streamers_info["data"]
        except ConnectionError as c_e:
            self.__logger.error(("Not able to connect to API. Verify your " "network."))
            sys.exit(1)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    def get_active_channels(self, streamers_info: dict) -> dict:
        statuses = {}
        self.__logger.debug("Obtaining channels status")
        try:
            for streamer in streamers_info:
                uid = streamer["id"]
                live_info_full = self.client.get_streams(user_id=uid)
                live_info = live_info_full["data"]
                if len(live_info):
                    statuses[uid] = live_info[0]
            self.__logger.debug("Obtained channels status:")
            self.__logger.debug(statuses)
            return statuses
        except ConnectionError as c_e:
            self.__logger.error(("Not able to connect to API. Verify your " "network."))
            sys.exit(1)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    # As pytwitchapi accepts 100 users as maximum, we need to regroup the whole list
    # into groups of 100 elements and join the results
    def __get_users(self, twitch_users: List[str]) -> dict:
        streamers_groups = [
            twitch_users[i : i + 100] for i in range(0, len(twitch_users), 100)
        ]
        streamers_info: dict = {}

        for group in streamers_groups:
            obtained_results = self.client.get_users(logins=group)
            for key, value in obtained_results.items():
                if key in streamers_info:
                    streamers_info[key].extend(value)
                else:
                    streamers_info[key] = value

        return streamers_info
