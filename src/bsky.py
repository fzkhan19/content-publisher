import os
from dotenv import load_dotenv
from platforms.bluesky_handler import BlueskyHandler

if __name__ == "__main__":
    load_dotenv()
    credentials = type(
        "Credentials",
        (),
        {
            "BLUESKY_HANDLE": os.getenv("BLUESKY_HANDLE"),
            "BLUESKY_APP_PASSWORD": os.getenv("BLUESKY_APP_PASSWORD"),
        },
    )
    handler = BlueskyHandler(credentials)
    # Call the post function to start the process
    handler.post("This is a test post via the automated Bluesky API flow. #test")
