import os
from dotenv import load_dotenv
from platforms.linkedin_handler import LinkedInHandler

if __name__ == "__main__":
    load_dotenv()
    credentials = type(
        "Credentials",
        (),
        {
            "LINKEDIN_CLIENT_ID": os.getenv("LINKEDIN_CLIENT_ID"),
            "LINKEDIN_CLIENT_SECRET": os.getenv("LINKEDIN_CLIENT_SECRET"),
        },
    )
    handler = LinkedInHandler(credentials)

    # Call the post function to start the process
    handler.post("This is a test post via the automated LinkedIn API flow.")
