import pytest


from tab import helpers


TWEET_SKELETON = "{custom_name}{1}{twitter_handle_with_at_enclosed}{1}tá on na Twitch. O título da live é: {livestream_title}. Bora!\n\n{twitch_url}\n{twitch_url}"
FULL_EXPECTED_RESULT = "Testing User (@TheTester) tá on na Twitch. O título da live é: Testing my live right now !test. Bora!\n\ntwitch.tv/thetester\ntwitch.tv/thetester"
NO_CUSTOM_EXPECTED_RESULT = "testing (@TheTester) tá on na Twitch. O título da live é: Testing my live right now !test. Bora!\n\ntwitch.tv/thetester\ntwitch.tv/thetester"
NO_TWITTER_EXPECTED_RESULT = "Testing User tá on na Twitch. O título da live é: Testing my live right now !test. Bora!\n\ntwitch.tv/thetester\ntwitch.tv/thetester"
NO_CUSTOM_TWITTER_EXPECTED_RESULT = "testing tá on na Twitch. O título da live é: Testing my live right now !test. Bora!\n\ntwitch.tv/thetester\ntwitch.tv/thetester"


def test_tweet_full_data(full_data):
    result = helpers.generate_tweet_message(TWEET_SKELETON, full_data)
    assert result == FULL_EXPECTED_RESULT


def test_tweet_no_custom_data(no_custom_name_data):
    result = helpers.generate_tweet_message(TWEET_SKELETON, no_custom_name_data)
    assert result == NO_CUSTOM_EXPECTED_RESULT 


def test_tweet_no_twitter_data(no_twitter_handle_data):
    result = helpers.generate_tweet_message(TWEET_SKELETON, no_twitter_handle_data)
    assert result == NO_TWITTER_EXPECTED_RESULT 


def test_tweet_no_custom_twitter_data(no_custom_twitter_data):
    result = helpers.generate_tweet_message(TWEET_SKELETON, no_custom_twitter_data)
    assert result == NO_CUSTOM_TWITTER_EXPECTED_RESULT