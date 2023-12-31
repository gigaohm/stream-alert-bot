import sys
from logging import Logger, getLogger
from twitter import Api, TwitterError
from typing import List

from sab import constants


class TwitterPublisher:
    client: Api = None
    twitter_id: str = ""
    tweet_count: int = constants.TWEET_COUNT

    __logger: Logger

    def __init__(self, credentials: dict, extra_settings: dict):
        try:
            consumer_key = credentials["consumer_key"]
            consumer_secret = credentials["consumer_secret"]
            access_key = credentials["access_key"]
            access_secret = credentials["access_secret"]
            twitter = Api(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token_key=access_key,
                access_token_secret=access_secret,
                # Needed to obtain the full text from tweets
                tweet_mode="extended",
            )
            self.__logger = getLogger(("stream-alert-bot/api/publishers/" "twitter"))
            self.__logger.debug("Twitter connection generated")
            self.client = twitter
            if "user" in extra_settings:
                self.__logger.debug("Found user info on extra settings")
                user_name = extra_settings["user"]
                self.__logger.debug(
                    " ".join(["Obtaining Twitter ID for user", user_name])
                )
                lookup_result = self.client.UsersLookup(screen_name=user_name)
                if len(lookup_result) == 0:
                    raise ValueError("The user name list is empty.")
                # We will always pick the first result
                self.__logger.debug("Obtained user ID")
                self.twitter_id = lookup_result[0].id
            if "tweet_count" in extra_settings:
                self.__logger.debug("Found tweet count on extra settings")
                self.tweet_count = extra_settings["tweet_count"]

        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)

    def post_message(self, message: str) -> bool:
        try:
            if self.twitter_id == "":
                self.__logger.warn(
                    "User ID has not been provided. There could be duplicated tweets if you are using this on multiple instances."
                )
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

    def __is_message_duplicated(self, message: str) -> bool:
        try:
            latest_tweets = self.client.GetUserTimeline(
                user_id=self.twitter_id,
                count=self.tweet_count,
                include_rts=False,
                trim_user=True,
                exclude_replies=True,
            )
            msg_to_post = message.split("\n")[0]
            for tweet in latest_tweets:
                if msg_to_post == tweet.full_text.split("\n")[0]:
                    return True

        except TwitterError as tt_e:
            # Twitter Errors are all accumulated into a single error
            self.__handle_twitter_errors(tt_e)
        except Exception as e:
            self.__logger.exception(e)
            sys.exit(1)
        return False

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
