import os
from dotenv import load_dotenv
from src.platforms.twitter_handler import TwitterHandler


def test_twitter_connection():
    try:
        # Create credentials object
        class Credentials:
            def __init__(self):
                self.TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
                self.TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
                self.TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
                self.TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

        # Initialize Twitter handler
        twitter = TwitterHandler(Credentials())

        # Test API connection with a simple me() call
        user = twitter.client.get_me()
        print(f"Successfully connected to Twitter as user ID: {user.data.id}")
        return twitter
    except Exception as e:
        print(f"Failed to connect to Twitter: {e}")
        return None


def make_test_post(content):
    if not content:
        raise ValueError("Content is required to make a post.")

    twitter = test_twitter_connection()
    if twitter:
        try:
            post_content = content
            success = twitter.post(post_content)
            if success:
                print("Post successfully published to Twitter!")
                return True
            else:
                print("Failed to publish post")
                return False
        except Exception as e:
            print(f"Error making post: {e}")
            return False


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Run the test post
    make_test_post()
