import re
from logging import getLogger
from twitter import Api
from typing import List

from sab import constants
from sab.api import connect_to_twitter, post_twitter_status


logger = getLogger("stream-alert-bot/helpers/functionality")


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
def check_finished_streams(old_livestreams: dict,
                           new_livestreams: dict,
                           consumer_type: str) -> bool:
    user_key = constants.CONSUMER_KEYS_TRANSLATION["username"][consumer_type]
    print(user_key)
    logger.debug("Checking for finished streams")
    for id in old_livestreams.keys():
        if id not in new_livestreams:
            logger.debug(" ".join(["Finished:",
                                   old_livestreams[id][user_key]]))
    return True


# Verify what streams are now live
def check_started_streams(consumer_type: str,
                          publishers_connections: List[Api],
                          old_livestreams: dict,
                          new_livestreams: dict,
                          streamers_info: dict,
                          message: str) -> bool:
    user_key = constants.CONSUMER_KEYS_TRANSLATION["userlogin"][consumer_type]
    logger.debug("Checking for started streams")
    for id in new_livestreams.keys():
        if id not in old_livestreams:
            stream = new_livestreams[id]
            streamer_key = stream[user_key]
            if consumer_type == "trovo":
                streamer_key = streamer_key.lower()
            streamer_info = streamers_info[streamer_key]
            notify_new_livestream(consumer_type, stream, streamer_info,
                                  message, publishers_connections)
    return True


def notify_new_livestream(consumer_type: str,
                          livestream_details: dict,
                          streamer_info: dict,
                          message: str,
                          publishers_connections: List[Api]) -> bool:
    # Translations
    user_key = constants.CONSUMER_KEYS_TRANSLATION["username"][consumer_type]
    game_key = constants.CONSUMER_KEYS_TRANSLATION["gamename"][consumer_type]
    base_url = constants.CONSUMER_KEYS_TRANSLATION["url"][consumer_type]
    title_key = constants.CONSUMER_KEYS_TRANSLATION["title"][consumer_type]
    login_key = constants.CONSUMER_KEYS_TRANSLATION["userlogin"][consumer_type]
    user_login = livestream_details[login_key]
    if consumer_type == "trovo":
        user_login = user_login.lower()

    # Custom patterns
    twitter_handle = streamer_info["twitter_handle"]
    custom_name = streamer_info["name"]
    user_name = livestream_details[user_key]

    info_dict = {
        "streamer_username": user_name,
        "custom_name": (custom_name if custom_name != ""
                        else user_name),
        "game_name": livestream_details[game_key],
        "stream_url": "".join([base_url, user_login]),
        "twitter_handle": twitter_handle,
        "livestream_title": livestream_details[title_key],
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
                           info_dict["streamer_username"],
                           "is live"]))
    formatted_message = generate_message(message, info_dict)
    logger.info(formatted_message)
    # TODO: Handle multiple publishers
    post_to_twitter(publishers_connections, formatted_message)


# Generates the tweet message
def generate_message(text, stream_info):
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
