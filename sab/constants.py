from trovoApi import TrovoClient
from twitchAPI.twitch import Twitch
from twitter import Api
from typing import List, Union


"""
TYPING TYPES
"""
consumer_types = Union[Twitch, TrovoClient]
publisher_types = List[Union[Api]]


"""
CONSTANTS
"""
PROGRAM_DESCRIPTION = "Alerts when a streamer is live"
CONSUMER_TYPES = ["trovo", "twitch"]
PUBLISHER_TYPES = ["twitter"]
ALL_SERVICES = CONSUMER_TYPES + PUBLISHER_TYPES
SERVICES_KEYS = {
    "trovo": [("client_id", "Client ID")],
    "twitch": [("client_id", "Client ID"), ("secret", "Secret")],
    "twitter": [
        ("consumer_key", "Consumer Key"),
        ("consumer_secret", "Consumer Secret"),
        ("access_key", "Access Key"),
        ("access_secret", "Access Secret"),
    ],
}
EXTRAS_KEYS = {"twitter": {"user": str, "tweet_count": int}}
CONSUMER_KEYS_TRANSLATION = {
    "username": {"trovo": "username", "twitch": "user_name"},
    "userlogin": {"trovo": "username", "twitch": "user_login"},
    "gamename": {"trovo": "category_id", "twitch": "game_name"},
    "title": {"trovo": "live_title", "twitch": "title"},
    "url": {"trovo": "trovo.live/", "twitch": "twitch.tv/"},
}
REPORT_MAX_TIME_INTERVAL = 600
POLLING_INTERVAL = 120
TWEET_COUNT = 5
