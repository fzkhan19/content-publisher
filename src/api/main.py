from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Dict, List

from src.platforms.bluesky_handler import BlueskyHandler
from src.platforms.linkedin_handler import LinkedInHandler
from src.platforms.twitter_handler import TwitterHandler
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()


class PostRequest(BaseModel):
    content: str
    platforms: List[str]


@app.post("/publish")
async def publish_content(
    request: PostRequest,
    x_twitter_api_key: str = Header(None),
    x_twitter_api_secret: str = Header(None),
    x_twitter_access_token: str = Header(None),
    x_twitter_access_token_secret: str = Header(None),
    x_linkedin_token: str = Header(None),
    x_bluesky_handle: str = Header(None),
    x_bluesky_password: str = Header(None),
):
    handlers = {}
    results = {}

    logger.debug(f"Received request to post to platforms: {request.platforms}")

    if "twitter" in request.platforms:
        logger.debug("Initializing Twitter handler")
        handlers["twitter"] = TwitterHandler(
            x_twitter_api_key,
            x_twitter_api_secret,
            x_twitter_access_token,
            x_twitter_access_token_secret,
        )

    if "bluesky" in request.platforms and x_bluesky_handle and x_bluesky_password:
        logger.debug("Initializing Bluesky handler")
        handlers["bluesky"] = BlueskyHandler(x_bluesky_handle, x_bluesky_password)

    if "linkedin" in request.platforms and x_linkedin_token:
        logger.debug("Initializing LinkedIn handler")
        handlers["linkedin"] = LinkedInHandler(x_linkedin_token)

    for platform, handler in handlers.items():
        logger.debug(f"Attempting to post to {platform}")
        success = handler.post(request.content)
        results[platform] = success
        logger.debug(f"Post to {platform} {'successful' if success else 'failed'}")

    successful = [p for p, success in results.items() if success]
    failed = [p for p, success in results.items() if not success]

    return {
        "status": (
            "success"
            if successful
            else "partial_failure" if successful and failed else "failure"
        ),
        "successful_posts": successful,
        "failed_posts": failed,
    }
