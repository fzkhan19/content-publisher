from bsky_bridge import BskySession, post_text


class BlueskyHandler:
    def __init__(self, credentials):
        self.handle = credentials.BLUESKY_HANDLE
        self.password = credentials.BLUESKY_APP_PASSWORD

    def post(self, content):
        try:
            session = BskySession(self.handle, self.password)
            response = post_text(session, content)
            return response
        except Exception as e:
            print(f"Error posting to Bluesky: {e}")
            return False
