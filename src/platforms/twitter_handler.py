import tweepy


class TwitterHandler:
    def __init__(self, credentials):
        self.client = tweepy.Client(
            consumer_key=credentials.TWITTER_API_KEY,
            consumer_secret=credentials.TWITTER_API_SECRET,
            access_token=credentials.TWITTER_ACCESS_TOKEN,
            access_token_secret=credentials.TWITTER_ACCESS_SECRET
        )

    def post(self, content):
        try:
            response = self.client.create_tweet(text=content)
            return True
        except Exception as e:
            print(f"Error posting to Twitter: {e}")
            return False
