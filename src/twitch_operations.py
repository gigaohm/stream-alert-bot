from twitchAPI.twitch import Twitch
from twitchAPI.webhook import TwitchWebHook


def connectToTwitch(client_id, secret):
    twitch = Twitch(client_id, secret)
    twitch.authenticate_app([])
    return twitch


def get_all_streamers_info(twitch_connection, streamers):
    # Get all streamers info
    twitch_users = [user["twitch_user"] for user in streamers]
    streamers_info = twitch_connection.get_users(logins=twitch_users)
    return streamers_info["data"]


def get_live_streams(twitch_connection, users_info):
    live_streams = {}
    for user in users_info:
        uid = user["id"]
        live_info = twitch_connection.get_streams(user_id=uid)["data"]
        if len(live_info):
            live_streams[uid] = live_info[0]

    return live_streams