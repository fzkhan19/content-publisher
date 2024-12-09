import os
from dotenv import load_dotenv
from platforms.linkedin_handler import LinkedInHandler

if __name__ == "__main__":
    load_dotenv()
    credentials = type('Credentials', (), {
        'LINKEDIN_CLIENT_ID': os.getenv("LINKEDIN_CLIENT_ID"),
        'LINKEDIN_CLIENT_SECRET': os.getenv("LINKEDIN_CLIENT_SECRET")
    })
    linkedin_handler = LinkedInHandler(credentials)

    # Authenticate and fetch person_id
    linkedin_handler.authenticate()

    # Post content
    linkedin_handler.post("Hello, LinkedIn! This is a test post.")
