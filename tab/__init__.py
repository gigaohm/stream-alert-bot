import sys
import time

import tab.api
import tab.helpers

def main():
    args = helpers.parse_parameters()
    settings = helpers.load_yaml(args.settings_file_path)

    twitch_creds = settings["credentials"]["twitch"]
    twitter_creds = settings["credentials"]["twitter"]
    polling_interval = settings["polling"]["interval"]
    streamers = settings["streamers"]
    streamers_info_dict = helpers.generate_streamers_info_dict(streamers)

    # Authenticate on twitch
    twitch = api.connect_to_twitch(twitch_creds["client_id"],
                                   twitch_creds["secret"])

    # Initial state
    streamers_info = api.get_all_streamers_info(twitch, streamers)
    previous_live_streams = api.get_live_streams(twitch, streamers_info)

    # Poll channel changes
    while True:
        try:
            current_live_streams = api.get_live_streams(twitch, streamers_info)
            helpers.check_finished_streams(previous_live_streams, current_live_streams)
            helpers.check_started_streams(twitter_creds, previous_live_streams,
                                  current_live_streams, streamers_info_dict)
            previous_live_streams = current_live_streams
        except Exception as e:
            print("Error: {}".format(e))

        time.sleep(polling_interval)

if __name__ == "__main__":
    sys.exit(main())
