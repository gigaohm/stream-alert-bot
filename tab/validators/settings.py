from logging import getLogger
import sys
import time

import tab.api
import tab.helpers

logger = getLogger("twitch-alert-bot/validators/settings")


def verify_settings(settings):
    logger.debug("First, validate we are getting a dict")
    if not isinstance(settings, dict):
        raise TypeError("Loaded settings are not a dictionary")
    logger.debug("Validating required keys on settings")
    # Validate credentials key existance
    logger.debug(("Validating the existance of the credentials key in the "
                  "settings"))
    if "credentials" not in settings:
        raise KeyError("Credentials key not found on settings file.")
    # Validating streamers key existance
    logger.debug(("Validating the existance of the streamers key in the "
                  "settings"))
    if "streamers" not in settings:
        raise KeyError("Streamers key not found on settings file.")
    # Validating message key existance
    logger.debug(("Validating the existance of the message key in the "
                  "settings"))
    if "message" not in settings:
        raise KeyError("Message key not found on settings file.")
    logger.debug("Required keys (credentials, streamers, message) are present")

    # Log warning for polling_interval
    if "polling_interval" not in settings:
        logger.warn(("Polling interval not provided. Will use default value "
                     "(120)."))

    # Now validating the content of the whole settings file
    for key in settings.keys():
        if key not in ["credentials", "polling_interval", "streamers",
                       "message"]:
            raise KeyError("".join(["Provided key (", key,
                                    (") is not one of the following: "
                                     "credentials, polling_interval, "
                                     "message, streamers")]))
        else:
            # Send to correct key validation
            if key == "credentials":
                validate_credentials(settings[key])
            elif key == "polling_interval":
                validate_polling_interval(settings[key])
            elif key == "streamers":
                validate_streamers(settings[key])
            elif key == "message":
                validate_message(settings[key])
            else:
                raise ValueError("".join(["Processed key (",
                                          key,
                                          (") was processed but it is unknown."
                                           " Contact developer.")]))


def validate_credentials(credentials):
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


def validate_polling_interval(interval):
    if not isinstance(interval, int):
        raise ValueError("Provided polling value is not an integer.")
    if interval <= 0:
        raise ValueError("Provided polling value is lower or equal to 0.")
    logger.debug("".join(["Polling interval on the settings is valid (",
                          str(interval),
                          ")"]))


def validate_message(message):
    if "text" not in message:
        raise KeyError("Key text is not provided.")
    # TODO: Handle custom_patterns here
    logger.debug("Provided message settings are valid")


def validate_streamers(streamers):
    for streamer in streamers:
        # Handle if streamer is a dict
        if not isinstance(streamer, dict) and not isinstance(streamer, str):
            raise ValueError("Provided streamer info is not correct.")
        else:
            if isinstance(streamer, dict):
                if len(streamer.keys()) > 1:
                    raise ValueError(("Streamer info has strange format (more "
                                      "than 1 key)"))
                for key, value in streamer.items():
                    logger.debug(" ".join(["Verifying streamer", key]))
                    for key in value.keys():
                        if key not in ["name", "twitter_handle"]:
                            raise KeyError("".join(["Provided key (",
                                                    key,
                                                    (") is not valid. It "
                                                     "should be one of the "
                                                     "following: name, twitter"
                                                     "_handle.")]))
    logger.debug("Streamers information is correct")


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
