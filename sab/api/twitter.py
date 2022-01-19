from logging import getLogger
import sys
import twitter


logger = getLogger("stream-alert-bot/api/twitter")


def connect_to_twitter(consumer_key, consumer_secret, access_key,
                       access_secret):
    try:
        logger.debug(" ".join(["Generating Twitter connection",
                               "(This does not ensure it works)"]))
        connection = twitter.Api(consumer_key=consumer_key,
                                 consumer_secret=consumer_secret,
                                 access_token_key=access_key,
                                 access_token_secret=access_secret)
        logger.debug("Twitter connection generated")
        return connection
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


def post_twitter_status(twitter_connection, message):
    try:
        logger.debug("Posting message to Twitter")
        status = twitter_connection.PostUpdate(message)
        logger.debug("Message posted successfully")
    except twitter.TwitterError as tt_e:
        # Twitter Errors are all accumulated into a single error
        handle_twitter_errors(tt_e)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


def handle_twitter_errors(twitter_error):
    # Twitter Errors are all accumulated into a single error
    error_code = twitter_error.message[0]["code"]
    error_message = twitter_error.message[0]["message"]
    logger.error(" ".join(["python-twitter error: Code",
                           str(error_code),
                           "-",
                           error_message]))
    '''
    Error codes that can be ignored
    187: Status is duplicated


    Error codes that cannot be ignored
    32: Could not authenticate you
    '''
    if error_code in [32]:
        sys.exit(1)
