PROGRAM_DESCRIPTION = "Alerts when a streamer is live"
CONSUMER_TYPES = ["trovo", "twitch"]
PUBLISHER_TYPES = ["twitter"]
ALL_SERVICES = CONSUMER_TYPES + PUBLISHER_TYPES
SERVICES_KEYS = {
    "trovo": [("client_id", "Client ID")],
    "twitch": [("client_id", "Client ID"), ("secret", "Secret")],
    "twitter": [("consumer_key", "Consumer Key"),
                ("consumer_secret", "Consumer Secret"),
                ("access_key", "Access Key"),
                ("access_secret", "Access Secret")]
}
