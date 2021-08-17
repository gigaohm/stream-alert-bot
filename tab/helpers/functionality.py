from tab.api import connect_to_twitter, post_twitter_status


def generate_streamers_info_dict(streamers):
    info_dict = {}
    for streamer in streamers:
        info_dict[streamer["twitch_user"]] = {"twitter_handle": (streamer["twitter_handle"] if "twitter_handle" in streamer else ""),
		                                      "name": (streamer["name"] if "name" in streamer else "")}
    return info_dict


def generate_tweet_message(streamer_name, twitter_handle, title, twitch_user):
	return "{0}{1} tá on na Twitch. O título da live é: \"{2}\". Bora!\n\nhttps://twitch.tv/{3}\nhttps://twitch.tv/{3}\n".format(streamer_name, twitter_handle, title, twitch_user)


def post_to_twitter(twitter_creds, message):
	twitter = connect_to_twitter(twitter_creds["consumer_key"],
                                            twitter_creds["consumer_secret"],
                                            twitter_creds["access_key"],
                                            twitter_creds["access_secret"])
	post_twitter_status(twitter, message)


# TODO: Use this function for logging
# Can be also used later to respond original tweet
def check_finished_streams(old_livestreams, new_livestreams):
    # Check finished live streams
    for uid in old_livestreams.keys():
        if uid not in new_livestreams:
            print("Finalizou: {0}".format(old_livestreams[uid]["user_name"]))


def check_started_streams(twitter_creds, old_livestreams, new_livestreams,
                          streamers_info):
    # Check new live streams
    for uid in new_livestreams.keys():
        if uid not in old_livestreams:
            stream = new_livestreams[uid]
            custom_streamer_name = streamers_info[stream["user_login"]]["name"]
            twitter_handle = streamers_info[stream["user_login"]]["twitter_handle"]
            streamer_name = custom_streamer_name if custom_streamer_name != "" else stream["user_name"]
            twitter_handle = " (@{})".format(twitter_handle) if twitter_handle != "" else ""
            message = generate_tweet_message(streamer_name, twitter_handle,
                                             stream["title"], stream["user_login"])
            print(message)
            post_to_twitter(twitter_creds, message)
