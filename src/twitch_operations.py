from twitchAPI.twitch import Twitch
from twitchAPI.webhook import TwitchWebHook


def connectToTwitch(client_id, secret):
    twitch = Twitch(client_id, secret)
    twitch.authenticate_app([])
    return twitch


def generate_streamers_info_dict(streamers):
    info_dict = {}
    for streamer in streamers:
        info_dict[streamer["twitch_user"]] = {"twitter_handle": (streamer["twitter_handle"] if "twitter_handle" in streamer else ""),
		                                      "name": (streamer["name"] if "name" in streamer else "")}
    return info_dict

def get_all_streamers_info(twitch_connection, streamers):
    # Get all streamers info
    twitch_users = [user["twitch_user"] for user in streamers]
    streamers_twitch_info = twitch_connection.get_users(logins=twitch_users)["data"]
    streamers_extra_info = generate_streamers_info_dict(streamers)
    return [{ **streamer, **streamers_extra_info[streamer["login"]]} for streamer in streamers_twitch_info]


def get_live_status(twitch_connection, users_info):
    live_status = {}
    for user in users_info:
        uid = user["id"]
        channel_info = twitch_connection.get_streams(user_id=uid)["data"]
        if len(channel_info):
            live_status[uid] = channel_info[0]

    return live_status


def process_live_status(old_live_status, new_live_status):
    # Check finished live streams
    for uid in old_live_status.keys():
        if uid not in new_live_status:
            stream = old_live_status[uid]
            print("Finalizou: {0}".format(stream["user_name"]))

    # Check new live streams
    for uid in new_live_status.keys():
        if uid not in old_live_status:
            stream = new_live_status[uid]
            # TODO: post to twitter
            print("{0}{1} tá on na Twitch. O título da live é: \"{2}\". Bora!\n\nhttps://twitch.tv/{3}\nhttps://twitch.tv/{3}\n".format((stream["name"] if stream["name"] != "" else stream["user_name"]),
                                                                                                                                        (" ({})".stream["twitter_handle"] if stream["twitter_handle"] != "" else ""),
                                                                                                                                        stream["title"],
                                                                                                                                        stream["user_login"]))