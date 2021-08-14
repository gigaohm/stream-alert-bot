import twitter


def connect_to_twitter(consumer_key, consumer_secret, access_key,
                       access_secret):
    return twitter.Api(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token_key=access_key,
                       access_token_secret=access_secret)


def post_twitter_status(twitter_connection, message):
    try:
        twitter_connection.PostUpdate(message)
    except twitter.TwitterError as tterror:
        print(tterror)
