from logging import getLogger
import sys
import time

import tab.api
import tab.helpers

logger = getLogger("twitch-alert-bot/validators/settings")


def verify_settings(settings):
    # Validate credentials key
    logger.debug("Validating the existance of credentials in the settings")
    if "credentials" not in settings:
        raise KeyError("Credentials not provided on settings file.")
    credentials = settings["credentials"]

    # Validating Twitch credentials
    logger.debug(("Validating the existance of Twitch credentials in the "
                  "settings"))
    if "twitch" not in credentials:
        raise KeyError(("Twitch credentials not found. They should be on the "
                        "settings file as credentials.twitch."))
    validate_twitch_credentials_settings(credentials["twitch"])
    logger.debug("Twitch credentials on the settings are complete")

    # Validating Twitter credentials
    logger.debug(("Validating the existance of Twitter credentials in the "
                  "settings"))
    if "twitter" not in credentials:
        raise KeyError(("Twitter credentials not found. They should be on the "
                        "settings file as credentials.twitter."))
    validate_twitter_credentials_settings(credentials["twitter"])
    logger.debug("Twitch credentials on the settings are complete")

    # Validating polling interval value
    logger.debug(("Validating if the polling interval (polling_interval) is "
                  "provided"))
    if "polling_interval" in settings:
        validate_polling_settings(settings["polling_interval"])
    else:
        logger.warn(("Polling interval not provided. Will use default value "
                     "(120)."))

    # Validating list of streamers
    logger.debug("Validating list of streamers")
    if "streamers" not in settings:
        raise KeyError(("Streamers key not found. They should be on the "
                        "settings file as streamers."))
    validate_streamers(settings["streamers"])
    logger.debug("Streamers information is correct")

    return True


def validate_twitch_credentials_settings(credentials):
    for key in [("client_id", "Client ID"), ("secret", "Secret")]:
        validate_keys(key[0],
                      "".join(["credentials.twitch.", key[0]]),
                      key[1],
                      "Twitch",
                      credentials)


def validate_twitter_credentials_settings(credentials):
    for key in [("consumer_key", "Consumer Key"),
                ("consumer_secret", "Consumer Secret"),
                ("access_key", "Access Key"),
                ("access_secret", "Access Secret")]:
        validate_keys(key[0],
                      "".join(["credentials.twitter.", key[0]]),
                      key[1],
                      "Twitter",
                      credentials)


def validate_polling_settings(polling):
    logger.debug("Validating if the polling interval value is higher than 0")
    if not isinstance(polling, int):
        raise ValueError("Provided polling value is not an integer.")
    if polling <= 0:
        raise ValueError("Provided polling value is lower or equal to 0.")
    logger.debug("".join(["Polling interval on the settings is valid (",
                          str(polling),
                          ")"]))


def validate_streamers(streamers):
    for streamer in streamers:
        if "twitch_user" not in streamer:
            raise KeyError(("Missing key twitch_user for streamer. It is "
                            "mandatory."))
        for key in streamer.keys():
            if key not in ["name", "twitter_handle", "twitch_user"]:
                raise KeyError(" ".join(["Provided key",
                                         key,
                                         "does not exist"]))


def validate_keys(key, key_path, pretty_name, service, dictionary):
    logger.debug(" ".join(["Validating the existance of",
                           service,
                           pretty_name]))
    if key not in dictionary:
        raise KeyError(" ".join([service,
                                 pretty_name,
                                 ("not found. It should be on the settings "
                                  "file as"),
                                 key_path]))
