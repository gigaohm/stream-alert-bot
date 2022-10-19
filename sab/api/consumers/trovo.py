import sys
from logging import Logger, getLogger
from requests.exceptions import ConnectionError
from trovoApi import TrovoClient, TrovoApiException


class TrovoConsumer:
    client: TrovoClient = None

    __logger: Logger

    def __init__(self, credentials: dict):
        try:
            client_id = credentials["client_id"]
            trovo = TrovoClient(client_id)
            self.__logger = getLogger("stream-alert-bot/api/consumers/trovo")
            self.__logger.debug("Connection to Trovo created")
            self.client = trovo
        except TrovoApiException as tr_e:
            self.__logger.error(
                "".join(["Trovo API gave the following ", "error: ", tr_e.message])
            )
            sys.exit(1)
        except ConnectionError as c_e:
            self.__logger.error(("Not able to connect to API. Verify your " "network"))
            sys.exit(1)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    def get_all_streamers_info(self, streamers: dict) -> dict:
        try:
            trovo_users = list(streamers.keys())
            self.__logger.debug("Obtaining streamers info")
            streamers_info = self.client.get_users(users=trovo_users)
            self.__logger.debug("Obtained streamers info:")
            self.__logger.debug(streamers_info)
            streamers = streamers_info.get("users")
            # Reap the user_id = 0 results
            for streamer in streamers:
                if int(streamer["user_id"]) == 0:
                    self.__logger.warn(
                        " ".join(
                            [
                                "Username",
                                streamer["username"],
                                "has a user_id 0. Ignoring.",
                            ]
                        )
                    )
                    # Ignoring this line as streamers is being recognized as a dict instead of list
                    streamers.remove(streamer)  # type: ignore[attr-defined]
            return streamers
        except TrovoApiException as tr_e:
            self.__logger.error(
                "".join(["Trovo API gave the following ", "error: ", tr_e.message])
            )
            sys.exit(1)
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
                chid = streamer["channel_id"]
                if chid == 0:
                    self.__logger.warn(
                        " ".join(
                            [
                                "Username",
                                streamer["username"],
                                "has a channel_id 0. Ignoring.",
                            ]
                        )
                    )
                    continue
                live_info = self.client.get_channel_info_by_id(channel_id=chid)
                # TODO: Add exception to TrovoApi error
                if live_info["is_live"]:
                    statuses[chid] = live_info
            self.__logger.debug("Obtained channels status:")
            self.__logger.debug(statuses)
            return statuses
        except TrovoApiException as tr_e:
            self.__logger.error(
                "".join(["Trovo API gave the following ", "error: ", tr_e.message])
            )
            sys.exit(1)
        except ConnectionError as c_e:
            self.__logger.error(("Not able to connect to API. Verify your " "network."))
            sys.exit(1)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)
