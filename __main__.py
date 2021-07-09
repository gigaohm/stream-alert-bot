#!/usr/bin/env python

from src import yaml_operations as yop, twitch_operations as twitch_a
import time

if __name__ == "__main__":
    # Get settings
    settings = yop.load_yaml_settings()

    twitch_creds = settings["credentials"]["twitch"]
    polling_interval = settings["polling"]["interval"]
    streamers = settings["streamers"]

    # Authenticate on twitch
    twitch = twitch_a.connectToTwitch(twitch_creds["client_id"],
                                      twitch_creds["secret"])

    # Initial state
    streamers_info = twitch_a.get_all_streamers_info(twitch, streamers)
    old_live_status = twitch_a.get_live_status(twitch, streamers_info)

    # Poll channel changes
    while True:
        new_live_status = twitch_a.get_live_status(twitch, streamers_info)
        twitch_a.process_live_status(old_live_status, new_live_status)
        old_live_status = new_live_status

        time.sleep(polling_interval)
