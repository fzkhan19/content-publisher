import os
from dotenv import load_dotenv


class Credentials:
    def __init__(self):

        load_dotenv()

        # X (Twitter) credentials
        self.TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
        self.TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
        self.TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
        self.TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

        # LinkedIn credentials
        self.LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")

        # Bluesky credentials
        self.BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
        self.BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")
