from logging import getLogger
import sys

from requests.exceptions import ConnectionError
from twitchAPI.twitch import Twitch
from twitchAPI.webhook import TwitchWebHook
from twitchAPI.types import TwitchAuthorizationException


logger = getLogger("twitch-alert-bot/api/twitch")


def connect_to_twitch(client_id, secret):
    try:
        logger.debug("Connecting to Twitch")
        twitch = Twitch(client_id, secret)
        twitch.authenticate_app([])
        logger.debug("Connection to Twitch successful")
        return twitch
    except TwitchAuthorizationException as ta_e:
        logger.error("Issues connecting to Twitch with provided credentials.")
        sys.exit(1)
    except ConnectionError as c_e:
        logger.error("Not able to connect to API. Verify your network.")
        sys.exit(1)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


def get_all_streamers_info(twitch_connection, streamers):
    try:
        twitch_users = list(streamers.keys())
        logger.debug("Obtaining streamers info")
        streamers_info = twitch_connection.get_users(logins=twitch_users)
        logger.debug("Obtained streamers info:")
        logger.debug(streamers_info)
        return streamers_info["data"]
    except ConnectionError as c_e:
        logger.error("Not able to connect to API. Verify your network.")
        sys.exit(1)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


def get_live_streams(twitch_connection, users_info):
    live_streams = {}
    logger.debug("Obtaining active livestreams")
    try:
        for user in users_info:
            uid = user["id"]
            live_info_full = twitch_connection.get_streams(user_id=uid)
            live_info = live_info_full["data"]
            if len(live_info):
                live_streams[uid] = live_info[0]
        logger.debug("Obtained active livestreams:")
        logger.debug(live_streams)
        return live_streams
    except ConnectionError as c_e:
        logger.error("Not able to connect to API. Verify your network.")
        sys.exit(1)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
