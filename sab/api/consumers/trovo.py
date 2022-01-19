from logging import Logger, getLogger
import sys

from requests.exceptions import ConnectionError
from trovoApi import TrovoClient


class TrovoConsumer:
    client: TrovoClient = None

    __logger: Logger = None

    def __init__(self,
                 credentials: dict):
        try:
            client_id = credentials["client_id"]
            trovo = TrovoClient(client_id)
            # TODO: Implement auth if possible
            # self.__logger.debug("Connection to Twitch successful")
            self.__logger = getLogger("stream-alert-bot/api/consumers/trovo")
            self.__logger.debug("Connection to Trovo created")
            self.client = trovo
        except ConnectionError as c_e:
            self.__logger.error(("Not able to connect to API. Verify your "
                                 "network"))
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    def get_all_streamers_info(self, streamers):
        try:
            trovo_users = list(streamers.keys())
            self.__logger.debug("Obtaining streamers info")
            streamers_info = self.client.get_users(users=trovo_users)
            self.__logger.debug("Obtained streamers info:")
            self.__logger.debug(streamers_info)
            return streamers_info["users"]
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
                chid = streamer["channel_id"]
                live_info = self.client.get_channel_info_by_id(channel_id=chid)
                # TODO: Add exception to TrovoApi error
                if live_info["is_live"]:
                    statuses[chid] = live_info
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
