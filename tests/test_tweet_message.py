from sab import helpers


TWEET_SKELETON = (
    "{custom_name}{1}{twitter_handle_with_at_enclosed}{1}tá on "
    "na Twitch. O título da live é: {livestream_title}. Bora!"
    "\n\n{twitch_url}\n{twitch_url}"
)
FULL_EXPECTED_RESULT = (
    "Testing User (@TheTester) tá on na Twitch. O título "
    "da live é: Testing my live right now !test. Bora!"
    "\n\ntwitch.tv/thetester\ntwitch.tv/thetester"
)
NO_CUSTOM_EXPECTED_RESULT = (
    "testing (@TheTester) tá on na Twitch. O título "
    "da live é: Testing my live right now !test. Bora!"
    "\n\ntwitch.tv/thetester\ntwitch.tv/thetester"
)
NO_TWITTER_EXPECTED_RESULT = (
    "Testing User tá on na Twitch. O título da "
    "live é: Testing my live right now !test. Bora!"
    "\n\ntwitch.tv/thetester\ntwitch.tv/thetester"
)
NO_CUSTOM_TWITTER_EXPECTED_RESULT = (
    "testing tá on na Twitch. O título da "
    "live é: Testing my live right now !test. Bora"
    "!\n\ntwitch.tv/thetester\ntwitch.tv/thetester"
)


def test_tweet_message_complete_data(streamer_test_data):
    result = helpers.generate_message(TWEET_SKELETON, streamer_test_data())
    print(result)
    assert result == FULL_EXPECTED_RESULT


def test_tweet_message_no_custom_name(streamer_test_data):
    result = helpers.generate_message(TWEET_SKELETON, streamer_test_data(False))
    print(result)
    assert result == NO_CUSTOM_EXPECTED_RESULT


def test_tweet_message_no_twitter_handle(streamer_test_data):
    result = helpers.generate_message(TWEET_SKELETON, streamer_test_data(True, False))
    print(result)
    assert result == NO_TWITTER_EXPECTED_RESULT


def test_tweet_message_no_optional_data(streamer_test_data):
    result = helpers.generate_message(TWEET_SKELETON, streamer_test_data(False, False))
    print(result)
    assert result == NO_CUSTOM_TWITTER_EXPECTED_RESULT
