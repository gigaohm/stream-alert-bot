import sys
from logging import Logger, getLogger
from twitter import Api, TwitterError
from typing import List


class TwitterPublisher:
    client: Api = None

    __logger: Logger = None

    def __init__(self, credentials: dict):
        try:
            consumer_key = credentials["consumer_key"]
            consumer_secret = credentials["consumer_secret"]
            access_key = credentials["access_key"]
            access_secret = credentials["access_secret"]
            twitter = Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_key,
                          access_token_secret=access_secret)
            self.__logger = getLogger(("stream-alert-bot/api/publishers/"
                                       "twitter"))
            self.__logger.debug("Twitter connection generated")
            self.client = twitter
        except Exception as e:
            logger.exception(e)
            sys.exit(1)

    def post_message(self, message: str) -> bool:
        try:
            self.__logger.debug("Posting message to Twitter")
            status = self.client.PostUpdate(message)
            self.__logger.debug("Message posted successfully")
        except TwitterError as tt_e:
            # Twitter Errors are all accumulated into a single error
            self.__handle_twitter_errors(tt_e)
        except Exception as e:
            logger.exception(e)
            sys.exit(1)
        return True

    def __handle_twitter_errors(self, twitter_error: TwitterError) -> None:
        # Twitter Errors are all accumulated into a single error
        error_code = twitter_error.message[0]["code"]
        error_message = twitter_error.message[0]["message"]
        self.__logger.error(" ".join(["python-twitter error: Code",
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
