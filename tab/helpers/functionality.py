from logging import getLogger
from tab.api import connect_to_twitter, post_twitter_status
import re


logger = getLogger("twitch-alert-bot/helpers/functionality")


def transform_streamers_to_dict(streamers):
    streamers_dict = {}
    for streamer in streamers:
        if isinstance(streamer, str):
            logger.debug(" ".join(["Streamer", streamer,
                                   "has no data provided"]))
            streamers_dict[streamer] = {"twitter_handle": "",
                                        "name": ""}
        else:
            for key, value in streamer.items():
                # Dealing with empty or nonexistant keys
                if "twitter_handle" not in value:
                    logger.debug(" ".join(["Streamer", key,
                                           "has no Twitter handle provided"]))
                    value["twitter_handle"] = ""
                if "name" not in value:
                    logger.debug(" ".join(["Streamer", key,
                                           "has no custom name provided"]))
                    value["name"] = ""
                streamers_dict[key] = value
    return streamers_dict


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
                          streamers_info, tweet):
    logger.debug("Checking for started streams")
    for uid in new_livestreams.keys():
        if uid not in old_livestreams:
            stream = new_livestreams[uid]
            streamer_info = streamers_info[stream["user_login"]]
            notify_new_livestream(stream, streamer_info, tweet,
                                  twitter_connection)


def notify_new_livestream(livestream_details, streamer_info, tweet,
                          twitter_connection):
    # Custom patterns
    twitter_handle = streamer_info["twitter_handle"]
    custom_name = streamer_info["name"]
    user_name = livestream_details["user_name"]
    info_dict = {
        "twitch_username": user_name,
        "custom_name": (custom_name if custom_name != ""
                        else user_name),
        "game_name": livestream_details["game_name"],
        "twitch_url": "".join(["twitch.tv/",
                               livestream_details["user_login"]]),
        "twitter_handle": twitter_handle,
        "livestream_title": livestream_details["title"],
        # Putting custom patterns here
        # TODO: Handle custom patterns through settings
        "twitter_handle_with_at": ("".join(["@", twitter_handle])
                                   if twitter_handle != "" else ""),
        "twitter_handle_with_at_enclosed": ("".join(["(@",
                                                     twitter_handle,
                                                     ")"])
                                            if twitter_handle != "" else "")
    }

    # Generate message and post to Twitter
    logger.debug(" ".join(["Found that",
                           info_dict["twitch_username"],
                           "is live"]))
    message = generate_tweet_message(tweet, info_dict)
    logger.info(message)
    post_to_twitter(twitter_connection, message)


# Generates the tweet message
def generate_tweet_message(text, stream_info):
    logger.debug("Generating Tweet Message")
    # Detecting key words
    for keyword in stream_info.keys():
        # TODO: Set this as a constant
        pattern = "".join([r"({\d+})?({", keyword, r"})({\d+})?"])
        result = re.finditer(pattern, text)
        for match in result:
            old_value = match.group()
            # Replace key words
            new_value = replace_keyword(old_value, stream_info, keyword)
            # Replace spaces if keyword exists
            if new_value != '':
                new_value = replace_space_keys(new_value)
            text = text.replace(old_value, new_value)
    return text


def replace_space_keys(text_to_replace):
    # Replace beginning
    m = re.findall(r"^{(\d+)}", text_to_replace)
    if m:
        spaces = ' ' * int(m[0])
        text_to_replace = re.sub(r"^{(\d+)}", spaces, text_to_replace)
    # Replace end
    m = re.findall(r"{(\d+)}$", text_to_replace)
    if m:
        spaces = ' ' * int(m[0])
        text_to_replace = re.sub(r"{(\d+)}$", spaces, text_to_replace)
    return text_to_replace


def replace_keyword(text_to_replace, value_dict, keyword):
    keyword_value = value_dict[keyword]
    if keyword_value != '':
        return re.sub("".join(["{", keyword, "}"]), keyword_value,
                      text_to_replace)
    else:
        return ''
