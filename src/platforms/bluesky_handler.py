import logging
from bsky_bridge import BskySession, post_text

logger = logging.getLogger(__name__)


class BlueskyHandler:
    def __init__(self, handle, password):
        logger.debug(f"Initializing Bluesky handler for handle: {handle}")
        self.handle = handle
        self.password = password
        logger.debug("Bluesky handler initialized")

    def post(self, content):
        try:
            logger.debug("Creating Bluesky session")
            session = BskySession(self.handle, self.password)
            logger.debug("Session created successfully")

            logger.debug(f"Attempting to post content: {content[:50]}...")
            response = post_text(session, content)
            logger.debug(f"Bluesky post response: {response}")

            return response
        except Exception as e:
            logger.error(f"Error posting to Bluesky: {str(e)}")
            return False
