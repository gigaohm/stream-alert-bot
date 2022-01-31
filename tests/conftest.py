import pytest


# Mandatory fields
USER_NAME = "testing"
GAME_NAME = "Testing Live"
USER_LOGIN = "thetester"
LIVESTREAM_TITLE = "Testing my live right now !test"

# Optional Fields
CUSTOM_NAME = "Testing User"
TWITTER_HANDLE = "TheTester"


@pytest.fixture()
# Strategy based on https://stackoverflow.com/a/51389067
def streamer_test_data():
    def get_streamer_test_data(enable_custom_name=True, enable_twitter_handle=True):
        return {
            "twitch_username": USER_NAME,
            "custom_name": (CUSTOM_NAME if enable_custom_name else USER_NAME),
            "game_name": GAME_NAME,
            "twitch_url": "".join(["twitch.tv/", USER_LOGIN]),
            "twitter_handle": (TWITTER_HANDLE if enable_twitter_handle else ""),
            "livestream_title": LIVESTREAM_TITLE,
            "twitter_handle_with_at": (
                "".join(["@", TWITTER_HANDLE]) if enable_twitter_handle else ""
            ),
            "twitter_handle_with_at_enclosed": (
                "".join(["(@", TWITTER_HANDLE, ")"]) if enable_twitter_handle else ""
            ),
        }

    return get_streamer_test_data
