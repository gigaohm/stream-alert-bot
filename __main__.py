#!./bin/python3

from src import yaml_operations as yop, twitch_operations as twitch_op, \
        functionality as f
import time


if __name__ == "__main__":
    # Get settings
    settings = yop.load_yaml_settings()

    twitch_creds = settings["credentials"]["twitch"]
    twitter_creds = settings["credentials"]["twitter"]
    polling_interval = settings["polling"]["interval"]
    streamers = settings["streamers"]
    streamers_info_dict = f.generate_streamers_info_dict(streamers)

    # Authenticate on twitch
    twitch = twitch_op.connectToTwitch(twitch_creds["client_id"],
                                      twitch_creds["secret"])

    # Initial state
    streamers_info = twitch_op.get_all_streamers_info(twitch, streamers)
    previous_live_streams = twitch_op.get_live_streams(twitch, streamers_info)

    # Poll channel changes
    while True:
        current_live_streams = twitch_op.get_live_streams(twitch, streamers_info)
        f.check_finished_streams(previous_live_streams, current_live_streams)
        f.check_started_streams(twitter_creds, previous_live_streams,
                                 current_live_streams, streamers_info_dict)
        previous_live_streams = current_live_streams

        time.sleep(polling_interval)
