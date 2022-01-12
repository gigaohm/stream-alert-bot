import pytest


# Mandatory fields
USER_NAME = "testing" 
GAME_NAME = "Testing Live"
USER_LOGIN = "thetester"
LIVESTREAM_TITLE = "Testing my live right now !test"

#Optional Fields
CUSTOM_NAME = "Testing User"
TWITTER_HANDLE = "TheTester"


@pytest.fixture()
def full_data():
    return {
        "twitch_username": USER_NAME,
        "custom_name": CUSTOM_NAME,
        "game_name": GAME_NAME,
        "twitch_url": "".join(["twitch.tv/",
                               USER_LOGIN]),
        "twitter_handle": TWITTER_HANDLE,
        "livestream_title": LIVESTREAM_TITLE,
        "twitter_handle_with_at": "".join(["@", TWITTER_HANDLE]),
        "twitter_handle_with_at_enclosed": "".join(["(@", TWITTER_HANDLE, ")"])
    }


@pytest.fixture
def no_custom_name_data():
    return {
        "twitch_username": USER_NAME,
        "custom_name": USER_NAME,
        "game_name": GAME_NAME,
        "twitch_url": "".join(["twitch.tv/",
                               USER_LOGIN]),
        "twitter_handle": TWITTER_HANDLE,
        "livestream_title": LIVESTREAM_TITLE,
        "twitter_handle_with_at": "".join(["@", TWITTER_HANDLE]),
        "twitter_handle_with_at_enclosed": "".join(["(@", TWITTER_HANDLE, ")"])
    }


@pytest.fixture
def no_twitter_handle_data():
    return {
        "twitch_username": USER_NAME,
        "custom_name": CUSTOM_NAME,
        "game_name": GAME_NAME,
        "twitch_url": "".join(["twitch.tv/",
                               USER_LOGIN]),
        "twitter_handle": "",
        "livestream_title": LIVESTREAM_TITLE,
        "twitter_handle_with_at": "",
        "twitter_handle_with_at_enclosed": ""
    }


@pytest.fixture
def no_custom_twitter_data():
    return {
        "twitch_username": USER_NAME,
        "custom_name": USER_NAME,
        "game_name": GAME_NAME,
        "twitch_url": "".join(["twitch.tv/",
                               USER_LOGIN]),
        "twitter_handle": "",
        "livestream_title": LIVESTREAM_TITLE,
        "twitter_handle_with_at": "",
        "twitter_handle_with_at_enclosed": ""
    }