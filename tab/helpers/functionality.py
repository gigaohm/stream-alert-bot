from logging import getLogger
from tab.api import connect_to_twitter, post_twitter_status


logger = getLogger("twitch-alert-bot/helpers/functionality")

'''
Adapts the list of streamers in the format:
{ "twitch_user": { "twitter_handle": x, "name": y } }
'''


def generate_streamers_info_dict(streamers):
    info_dict = {}
    for streamer in streamers:
        info_dict[streamer["twitch_user"]] = {"twitter_handle": (streamer["twitter_handle"] if "twitter_handle" in streamer else ""),
                                              "name": (streamer["name"]
                                                       if "name" in streamer
                                                       else "")}
    logger.debug("Created streamer info dictionary:")
    logger.debug(info_dict)
    return info_dict


def post_to_twitter(twitter_connection, message):
    post_twitter_status(twitter_connection, message)


# Verifies which livestreams have been finished
def check_finished_streams(old_livestreams, new_livestreams):
    logger.debug("Checking for finished streams")
    for uid in old_livestreams.keys():
        if uid not in new_livestreams:
            logger.debug(" ".join(["Finished:",
                                   old_livestreams[uid]["user_name"]]))


# Verify what streams are now live
def check_started_streams(twitter_connection, old_livestreams, new_livestreams,
                          streamers_info):
    logger.debug("Checking for started streams")
    for uid in new_livestreams.keys():
        if uid not in old_livestreams:
            stream = new_livestreams[uid]
            streamer_info = streamers_info[stream["user_login"]]
            notify_new_livestream(stream, streamer_info, twitter_connection)


def notify_new_livestream(livestream_details, streamer_info,
                          twitter_connection):
    # Extract info from streamer_info
    custom_streamer_name = streamer_info["name"]
    twitter_handle = streamer_info["twitter_handle"]

    # Verify if streamer has custom name. If not, use Twitch user name
    streamer_name = (custom_streamer_name
                     if custom_streamer_name != ""
                     else livestream_details["user_name"])
    # Customize Twitter handle (if there's any) by adding at sign
    twitter_handle = (" (@{})".format(twitter_handle)
                      if twitter_handle != ""
                      else "")

    # Generate message and post to Twitter
    logger.debug(" ".join(["Found that",
                           livestream_details["user_login"],
                           "is live"]))
    message = generate_tweet_message(streamer_name, twitter_handle,
                                     livestream_details["title"],
                                     livestream_details["user_login"])
    logger.info(message)
    post_to_twitter(twitter_connection, message)


# Generates the tweet message
# TODO: Try to make it more customizable
def generate_tweet_message(streamer_name, twitter_handle, title, twitch_user):
    return "{0}{1} tá on na Twitch. O título da live é: \"{2}\". Bora! #ApagaoTwitch\n\nhttps://twitch.tv/{3}\nhttps://twitch.tv/{3}\n".format(streamer_name, twitter_handle, title, twitch_user)
