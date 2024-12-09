import requests
import webbrowser


class LinkedInHandler:
    def __init__(self, credentials):
        self.client_id = credentials.LINKEDIN_CLIENT_ID
        self.client_secret = credentials.LINKEDIN_CLIENT_SECRET
        self.access_token = None
        self.person_id = "RX0LlKHJl4"  # Replace with your actual person ID
        self.redirect_uri = "http://localhost:8080/code"
        self.authorization_code = None

    def get_authorization_code(self):
        """Open the browser to LinkedIn's authorization URL."""
        auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=w_member_social%20profile%20openid"
        print("Opening browser for LinkedIn authorization...")
        webbrowser.open(auth_url)

        # Manually enter the authorization code after granting access
        self.authorization_code = input("Enter the authorization code from the URL: ")

        print(f"Authorization code received: {self.authorization_code}")

    def authenticate(self):
        """Exchange the authorization code for an access token."""
        if not self.authorization_code:
            print(
                "Authorization code is not available. Please complete the authorization process."
            )
            return None

        url = "https://www.linkedin.com/oauth/v2/accessToken"
        payload = {
            "grant_type": "authorization_code",
            "code": self.authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        print(f"POST Request to {url} with payload: {payload}")
        response = requests.post(url, data=payload)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.json()}")

        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            print("Access Token Retrieved Successfully:", self.access_token)
        else:
            print("Failed to authenticate:", response.json())
            return None

        return self.access_token

    def post(self, content):
        """Post content to LinkedIn."""
        # Step 1: Get the authorization code and authenticate
        self.get_authorization_code()

        # Step 2: Authenticate and retrieve the access token
        self.authenticate()

        if not self.access_token:
            print("Access token not available. Please authenticate first.")
            return False

        if not self.person_id:
            print("Person ID not available. Cannot post.")
            return False

        print("Preparing to post content to LinkedIn...")
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

        print(f"POST Request to /ugcPosts with Headers: {headers}")
        print(f"Payload: {payload}")
        response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts", headers=headers, json=payload
        )

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.json()}")

        if response.status_code == 201:
            print("Post published successfully.")
            return True
        else:
            print("Failed to post:", response.json())
            return False
