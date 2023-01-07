import datetime
import logging
import sys
import time

from sab import api, constants, helpers, validators


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
        settings["polling_interval"]
        if "polling_interval" in settings
        else constants.POLLING_INTERVAL
    )
    report_accepted_interval = (
        settings["report_max_time_interval"]
        if "report_max_time_interval" in settings
        else constants.REPORT_MAX_TIME_INTERVAL
    )
    if polling_interval > report_accepted_interval:
        logger.error(
            "".join(
                [
                    "The polling interval is higher than the tolerated interval between reports (",
                    str(polling_interval),
                    " vs ",
                    str(report_accepted_interval),
                    "). Please edit your settings.",
                ]
            )
        )
        sys.exit(1)
    extras = settings["extras"] if "extras" in settings else {}
    msg_skeleton = settings["message"]["text"]
    streamers = helpers.transform_streamers_to_dict(settings["streamers"])

    # Generate connection to consumer/publishers
    consumer_client = api.create_consumer(args.consumer, consumer_creds, extras)
    publishers = api.create_publishers(publisher_creds, extras)

    # Initial livestream info
    logger.debug("Generating initial state of livestreams")
    report_time = datetime.datetime.now()
    streamers_info = consumer_client.get_all_streamers_info(streamers)
    previous_statuses = consumer_client.get_active_channels(streamers_info)

    # Poll channel changes
    while True:
        logger.debug("Polling and checking new livestreams")
        last_report_time = report_time
        report_time = datetime.datetime.now()
        interval_between_reports = (report_time - last_report_time).total_seconds()
        if interval_between_reports <= report_accepted_interval:
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
        else:
            logger.warning(
                "".join(
                    [
                        "This report overpassed the maximum time between reports (current interval of ",
                        str(interval_between_reports),
                        " vs max interval of ",
                        str(report_accepted_interval),
                        "). Ignoring results.",
                    ]
                )
            )
        logger.debug(" ".join(["Waiting", str(polling_interval), "seconds"]))
        time.sleep(polling_interval)


if __name__ == "__main__":
    sys.exit(main())
