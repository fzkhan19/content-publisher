import logging
import requests

logger = logging.getLogger(__name__)


class LinkedInHandler:
    def __init__(self, access_token):
        logger.debug("Initializing LinkedIn handler")
        self.access_token = access_token
        logger.debug("LinkedIn handler initialized with access token")

    def post(self, content):
        if not self.access_token:
            logger.error("Access token not available")
            return False

        logger.debug("Preparing to post content to LinkedIn")
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }
        payload = {
            "author": f"urn:li:person:{self.person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        logger.debug(f"Making POST request to LinkedIn API with payload: {payload}")
        response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts", headers=headers, json=payload
        )

        logger.debug(f"LinkedIn API response status: {response.status_code}")
        logger.debug(f"LinkedIn API response content: {response.json()}")

        if response.status_code == 201:
            logger.info("Successfully posted content to LinkedIn")
            return True
        else:
            logger.error(f"Failed to post to LinkedIn: {response.json()}")
            return False
