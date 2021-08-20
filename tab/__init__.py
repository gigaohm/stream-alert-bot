import logging
import sys
import time

import tab.api
import tab.helpers
import tab.validators


def main():
    # Obtain arguments
    args = helpers.parse_parameters()

    # Set up logger
    logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO))
    logger = logging.getLogger("twitch-alert-bot")

    # Obtain settings and adapt streamers list
    settings = helpers.load_yaml(args.settings_file_path)
    validators.verify_settings(settings)
    logger.debug("Settings verified, time to grab the data")
    twitch_creds = settings["credentials"]["twitch"]
    twitter_creds = settings["credentials"]["twitter"]
    polling_interval = (settings["polling_interval"]
                        if settings["polling_interval"] else 120)
    streamers = settings["streamers"]
    streamers_info_dict = helpers.generate_streamers_info_dict(streamers)

    # Authenticate to Twitch
    twitch = api.connect_to_twitch(twitch_creds["client_id"],
                                   twitch_creds["secret"])

    # Generate connection to Twitter
    twitter = api.connect_to_twitter(twitter_creds["consumer_key"],
                                     twitter_creds["consumer_secret"],
                                     twitter_creds["access_key"],
                                     twitter_creds["access_secret"])

    # Initial livestream info
    logger.debug("Generating initial state of livestreams")
    streamers_info = api.get_all_streamers_info(twitch, streamers)
    previous_live_streams = api.get_live_streams(twitch, streamers_info)

    # Poll channel changes
    while True:
        logger.debug("Polling and checking new livestreams")
        current_live_streams = api.get_live_streams(twitch, streamers_info)
        helpers.check_finished_streams(previous_live_streams,
                                       current_live_streams)
        helpers.check_started_streams(twitter, previous_live_streams,
                                      current_live_streams,
                                      streamers_info_dict)
        previous_live_streams = current_live_streams

        logger.debug(" ".join(["Waiting", str(polling_interval), "seconds"]))
        time.sleep(polling_interval)


if __name__ == "__main__":
    sys.exit(main())
