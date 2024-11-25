
import tweepy

class TwitterHandler:
    def __init__(self, credentials):
        self.auth = tweepy.OAuthHandler(
            credentials.TWITTER_API_KEY,
            credentials.TWITTER_API_SECRET
        )
        self.auth.set_access_token(
            credentials.TWITTER_ACCESS_TOKEN,
            credentials.TWITTER_ACCESS_SECRET
        )
        self.api = tweepy.API(self.auth)

    def post(self, content):
        try:
            self.api.update_status(content)
            return True
        except Exception as e:
            print(f"Error posting to Twitter: {e}")
            return False
