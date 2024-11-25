
import requests

class LinkedInHandler:
    def __init__(self, credentials):
        self.access_token = credentials.LINKEDIN_ACCESS_TOKEN
        self.user_id = credentials.LINKEDIN_USER_ID

    def post(self, content):
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            payload = {
                "author": f"urn:li:person:{self.user_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": content},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }
            response = requests.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers=headers,
                json=payload
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Error posting to LinkedIn: {e}")
            return False
