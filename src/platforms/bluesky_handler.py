
from atproto import Client

class BlueskyHandler:
    def __init__(self, credentials):
        self.client = Client()
        self.handle = credentials.BLUESKY_HANDLE
        self.password = credentials.BLUESKY_APP_PASSWORD

    def post(self, content):
        try:
            self.client.login(self.handle, self.password)
            self.client.send_post(content)
            return True
        except Exception as e:
            print(f"Error posting to Bluesky: {e}")
            return False
