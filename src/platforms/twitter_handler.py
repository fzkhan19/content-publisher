import tweepy
import logging

logger = logging.getLogger(__name__)


class TwitterHandler:
    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        logger.debug("Initializing Twitter client with provided credentials")
        try:
            self.client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )
            logger.debug("Twitter client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {str(e)}")
            raise

    def post(self, content):
        try:
            logger.debug(f"Attempting to post content: {content[:50]}...")
            response = self.client.create_tweet(text=content)
            logger.debug(f"Tweet posted successfully. Response: {response}")
            return True
        except Exception as e:
            logger.error(f"Error posting to Twitter: {str(e)}")
            return False
