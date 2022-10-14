import sys
from logging import Logger, getLogger
from twitter import Api, TwitterError
from typing import List


class TwitterPublisher:
    client: Api = None
    __user: str = None

    __logger: Logger

    def __init__(self, credentials: dict):
        try:
            consumer_key = credentials["consumer_key"]
            consumer_secret = credentials["consumer_secret"]
            access_key = credentials["access_key"]
            access_secret = credentials["access_secret"]
            # TODO: Obtain __user
            twitter = Api(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token_key=access_key,
                access_token_secret=access_secret,
                # Needed to obtain the full text from tweets
                tweet_mode='extended'
            )
            self.__logger = getLogger(("stream-alert-bot/api/publishers/" "twitter"))
            self.__logger.debug("Twitter connection generated")
            self.client = twitter
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    def post_message(self, message: str) -> bool:
        try:
            if __user is None:
                self.__logger.warn("User ID has not been provided. There could be duplicated tweets if you are using this on multiple instances.")
            elif self.__is_message_duplicated(message):
                self.__logger.warn("Message is a duplicate. Not posting.")
                return False
            self.__logger.debug("Posting message to Twitter")
            status = self.client.PostUpdate(message)
            self.__logger.debug("Message posted successfully")
        except TwitterError as tt_e:
            # Twitter Errors are all accumulated into a single error
            self.__handle_twitter_errors(tt_e)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)
        return True

    def __is_message_duplicate(self, message: str) -> bool:
        try:
            user = self.client.UsersLookup(screen_name=self.__user)
            if len(user) == 0:
                raise ValueError("The user name list is empty.")
            user_id = user[0].id
            # FIXME: See if it is needed to customize the count here
            latest_tweets = self.client.GetUserTimeline(user_id=user_id,
                                                        count=10,
                                                        include_rts=False,
                                                        trim_user=True,
                                                        exclude_replies=True)
            msg_to_post = message.split("\n")[0]
            for tweet in tweets:
                if msg_to_post == tweet.full_text.split("\n")[0]:
                    return True
            return False

        except TwitterError as tt_e:
            # Twitter Errors are all accumulated into a single error
            self.__handle_twitter_errors(tt_e)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    def __handle_twitter_errors(self, twitter_error: TwitterError) -> None:
        # Twitter Errors are all accumulated into a single error
        error_code = twitter_error.message[0]["code"]
        error_message = twitter_error.message[0]["message"]
        self.__logger.error(
            " ".join(
                ["python-twitter error: Code", str(error_code), "-", error_message]
            )
        )
        """
        Error codes that can be ignored
        187: Status is duplicated

        Error codes that cannot be ignored
        32: Could not authenticate you
        """
        if error_code in [32]:
            sys.exit(1)
