import logging
import sys
import time

from sab import api, helpers, validators


def main():
    # Obtain arguments
    args = helpers.parse_parameters()

    # Set up logger
    logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO))
    logger = logging.getLogger("stream-alert-bot")

    # Obtain settings and adapt streamers list
    settings = helpers.load_yaml(args.settings_file_path)
    validators.verify_settings(settings)
    logger.debug("Settings verified, time to grab the data")
    consumer_creds = validators.verify_consumer(args.consumer, settings["credentials"])
    publisher_creds = validators.verify_publishers(
        args.publishers, settings["credentials"]
    )
    polling_interval = (
        settings["polling_interval"] if "polling_interval" in settings else 120
    )
    msg_skeleton = settings["message"]["text"]
    streamers = helpers.transform_streamers_to_dict(settings["streamers"])

    # Generate connection to consumer/publishers
    consumer_client = api.create_consumer(args.consumer, consumer_creds)
    publishers = api.create_publishers(publisher_creds)

    # Initial livestream info
    logger.debug("Generating initial state of livestreams")
    streamers_info = consumer_client.get_all_streamers_info(streamers)
    previous_statuses = consumer_client.get_active_channels(streamers_info)

    # Poll channel changes
    while True:
        logger.debug("Polling and checking new livestreams")
        current_statuses = consumer_client.get_active_channels(streamers_info)
        helpers.check_finished_streams(
            previous_statuses, current_statuses, args.consumer
        )
        helpers.check_started_streams(
            args.consumer,
            publishers,
            previous_statuses,
            current_statuses,
            streamers,
            msg_skeleton,
        )
        previous_statuses = current_statuses

        logger.debug(" ".join(["Waiting", str(polling_interval), "seconds"]))
        time.sleep(polling_interval)


if __name__ == "__main__":
    sys.exit(main())
