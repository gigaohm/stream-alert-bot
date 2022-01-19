from logging import Logger, getLogger
import sys

from requests.exceptions import ConnectionError
from twitchAPI.twitch import Twitch
from twitchAPI.webhook import TwitchWebHook
from twitchAPI.types import TwitchAuthorizationException


class TwitchConsumer:
    client: Twitch = None

    __logger: Logger = None

    def __init__(self,
                 credentials: dict):
        try:
            client_id = credentials["client_id"]
            secret = credentials["secret"]
            twitch = Twitch(client_id, secret)
            twitch.authenticate_app([])
            self.__logger = getLogger("stream-alert-bot/api/consumers/twitch")
            self.__logger.debug("Connection to Twitch successful")
            self.client = twitch
        except TwitchAuthorizationException as ta_e:
            self.__logger.error(("Issues connecting to Twitch with provided "
                                 "credentials."))
            sys.exit(1)
        except ConnectionError as c_e:
            self.__logger.error(("Not able to connect to API. Verify your "
                                 "network."))
            sys.exit(1)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    def get_all_streamers_info(self, streamers):
        try:
            twitch_users = list(streamers.keys())
            self.__logger.debug("Obtaining streamers info")
            streamers_info = self.client.get_users(logins=twitch_users)
            self.__logger.debug("Obtained streamers info:")
            self.__logger.debug(streamers_info)
            return streamers_info["data"]
        except ConnectionError as c_e:
            self.__logger.error(("Not able to connect to API. Verify your "
                                 "network."))
            sys.exit(1)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    def get_active_channels(self, streamers_info):
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
            self.__logger.error(("Not able to connect to API. Verify your "
                                 "network."))
            sys.exit(1)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)
