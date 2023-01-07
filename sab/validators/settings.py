import typing
from logging import getLogger

import sab.api
import sab.helpers
from sab import constants

logger = getLogger("stream-alert-bot/validators/settings")


def verify_settings(settings: dict) -> bool:
    logger.debug("First, validate we are getting a dict")
    if not isinstance(settings, dict):
        raise TypeError("Loaded settings are not a dictionary")
    logger.debug("Validating required keys on settings")
    # Validate credentials key existance
    logger.debug(("Validating the existance of the credentials key in the " "settings"))
    if "credentials" not in settings:
        raise KeyError("Credentials key not found on settings file.")
    # Validating streamers key existance
    logger.debug(("Validating the existance of the streamers key in the " "settings"))
    if "streamers" not in settings:
        raise KeyError("Streamers key not found on settings file.")
    # Validating message key existance
    logger.debug(("Validating the existance of the message key in the " "settings"))
    if "message" not in settings:
        raise KeyError("Message key not found on settings file.")
    logger.debug("Required keys (credentials, streamers, message) are present")

    # Log warning for polling_interval
    if "polling_interval" not in settings:
        logger.warn(
            "".join(
                [
                    "Polling interval not provided. Will use default value (",
                    str(constants.POLLING_INTERVAL),
                    ").",
                ]
            )
        )

    # Log warning for report_max_time_interval
    if "report_max_time_interval" not in settings:
        logger.warn(
            "".join(
                [
                    "Max tolerated time between intervals not provided. Will use default value (",
                    str(constants.REPORT_MAX_TIME_INTERVAL),
                    ").",
                ]
            )
        )

    # Log warning for extras
    if "extras" not in settings:
        logger.warn(("Extras not provided. Will use default values."))

    # Now validating the content of the whole settings file
    for key, value in settings.items():
        if key not in [
            "credentials",
            "polling_interval",
            "report_max_time_interval",
            "streamers",
            "message",
            "extras",
        ]:
            raise KeyError(
                "".join(
                    [
                        "Provided key (",
                        key,
                        (
                            ") is not one of the following: "
                            "credentials, polling_interval, "
                            "report_max_time_interval, ",
                            "message, streamers, extras",
                        ),
                    ]
                )
            )
        else:
            # Send to correct key validation
            if key == "credentials":
                validate_credentials(value)
            elif key == "polling_interval":
                validate_polling_interval(value)
            elif key == "report_max_time_interval":
                validate_report_max_time_interval(value)
            elif key == "streamers":
                validate_streamers(value)
            elif key == "message":
                validate_message(value)
            elif key == "extras":
                validate_extras(value)
            else:
                raise ValueError(
                    "".join(
                        [
                            "Processed key (",
                            key,
                            (
                                ") was processed but it is unknown."
                                " Contact developer."
                            ),
                        ]
                    )
                )
    return True


"""
CREDENTIALS VALIDATORS
"""


def validate_credentials(credentials: dict) -> bool:
    logger.debug(("Validating all of the provided credentials"))
    has_valid_consumer = False
    has_valid_publisher = False
    for service, creds in credentials.items():
        if service not in constants.ALL_SERVICES:
            raise KeyError(
                "".join(
                    [
                        "Provided service (",
                        service,
                        ") is invalid. It must be one of ",
                        "these services: ",
                        ", ".join(constants.ALL_SERVICES),
                    ]
                )
            )
        if service in constants.CONSUMER_TYPES:
            logger.debug(" ".join(["Found", service.capitalize(), "credentials"]))
            has_valid_consumer = validate_service_credentials(service, creds)
            continue
        elif service in constants.PUBLISHER_TYPES:
            logger.debug(" ".join(["Found", service.capitalize(), "credentials"]))
            has_valid_publisher = validate_service_credentials(service, creds)
            continue
    if not has_valid_consumer:
        raise ValueError(
            "".join(
                [
                    "No consumer has been provided on the ",
                    "credentials. It must be one of these: ",
                    ", ".join(constants.CONSUMER_TYPES),
                ]
            )
        )
    if not has_valid_publisher:
        raise ValueError(
            "".join(
                [
                    "No publisher has been provided on the ",
                    "credentials. It must be one of these: ",
                    ", ".join(constants.PUBLISHER_TYPES),
                ]
            )
        )
    logger.debug(
        (
            "Credentials on the settings are valid, and has at least 1"
            " consumer and 1 publisher"
        )
    )
    return True


def validate_service_credentials(service_name: str, credentials: dict) -> bool:
    service_keys = constants.SERVICES_KEYS[service_name]
    base_key_path = ".".join(["credentials", service_name])
    capitalized_service_name = service_name.capitalize()
    for key in service_keys:
        validate_keys(
            key[0],
            ".".join([base_key_path, key[0]]),
            key[1],
            capitalized_service_name,
            credentials,
        )
    logger.debug(" ".join([capitalized_service_name, "credentials are valid"]))
    return True


"""
EXTRAS VALIDATOR
"""


def validate_extras(settings: dict) -> bool:
    try:
        extras_keys = constants.EXTRAS_KEYS
        # First validate the values from settings
        for key, value in settings.items():
            if key not in extras_keys:
                raise KeyError(
                    " ".join(["Provided key", key, "on extras is not valid"])
                )
            # Then validate the subkeys
            for subkey, subvalue in value.items():
                if subkey not in extras_keys[key]:
                    raise KeyError(
                        " ".join(["Provided subkey", subkey, "on", key, "is not valid"])
                    )
                if type(subvalue) != extras_keys[key][subkey]:
                    raise TypeError(
                        " ".join(
                            [
                                "Provided value for subkey",
                                subkey,
                                "is not of type",
                                str(extras_keys[key][subkey]),
                            ]
                        )
                    )
        logger.debug("Extras on the settings are valid")
    except Exception as e:
        logger.exception(e)
    return True


"""
POLLING INTERVAL VALIDATOR
"""


def validate_polling_interval(interval: int) -> bool:
    if not isinstance(interval, int):
        raise ValueError("Provided polling value is not an integer.")
    if interval <= 0:
        raise ValueError("Provided polling value is lower or equal to 0.")
    logger.debug(
        "".join(["Polling interval on the settings is valid (", str(interval), ")"])
    )
    return True


"""
REPORT MAX TOLERATED INTERVAL VALIDATOR
"""


def validate_report_max_time_interval(interval: int) -> bool:
    if not isinstance(interval, int):
        raise ValueError("Provided interval value is not an integer.")
    if interval <= 0:
        raise ValueError("Provided interval value is lower or equal to 0.")
    logger.debug(
        "".join(
            [
                "Provided tolerated interval on the settings is valid (",
                str(interval),
                ")",
            ]
        )
    )
    return True


"""
MESSAGE VALIDATOR
"""


def validate_message(message: str) -> bool:
    if "text" not in message:
        raise KeyError("Key text is not provided.")
    # TODO: Handle custom_patterns here
    logger.debug("Provided message settings are valid")
    return True


"""
STREAMERS VALIDATOR
"""


def validate_streamers(streamers: dict) -> bool:
    for streamer in streamers:
        # Handle if streamer is a dict
        if not isinstance(streamer, dict) and not isinstance(streamer, str):
            raise ValueError("Provided streamer info is not correct.")
        else:
            if isinstance(streamer, dict):
                if len(streamer.keys()) > 1:
                    raise ValueError(
                        ("Streamer info has strange format (more " "than 1 key)")
                    )
                for key, value in streamer.items():
                    logger.debug(" ".join(["Verifying streamer", key]))
                    for key in value.keys():
                        if key not in ["name", "twitter_handle"]:
                            raise KeyError(
                                "".join(
                                    [
                                        "Provided key (",
                                        key,
                                        (
                                            ") is not valid. It "
                                            "should be one of the "
                                            "following: name, twitter"
                                            "_handle."
                                        ),
                                    ]
                                )
                            )
    logger.debug("Streamers information is correct")
    return True


"""
MISC FUNCTIONS
"""


def validate_keys(
    key: str, key_path: str, pretty_name: str, service: str, dictionary: dict
) -> bool:
    logger.debug(" ".join(["Validating the existance of", service, pretty_name]))
    if key not in dictionary:
        raise KeyError(
            " ".join(
                [
                    service,
                    pretty_name,
                    ("not found. It should be on the settings " "file as"),
                    key_path,
                ]
            )
        )
    return True
