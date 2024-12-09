import requests


class LinkedInHandler:
    def __init__(self, credentials):
        self.client_id = credentials.LINKEDIN_CLIENT_ID
        self.client_secret = credentials.LINKEDIN_CLIENT_SECRET
        self.access_token = ""
        self.person_id = "RX0LlKHJl4"

    def authenticate(self):
        print("Authenticating with LinkedIn...")
        url = "https://www.linkedin.com/oauth/v2/accessToken"
        payload = {
            "grant_type": "authorization_code",
            "code": "AQS96_AyxBhcngC9wAP1P3tLjzp1f8kLKs62PYlgjIGthW-EO5_QxON775K4zGW8jOGaMMR15eWI8pCAilFeHAyahxdr1J3I0ndBwEQ_fHVI7-iwE5piwmfpy5yi9nvpatfIv-7jGPI1MP6c2qVwuZ7450oObLB0gol9NRTprYgl1-Iw_wnq0_I6KmKQy0Qalwwk1DzN_-HKFleEsq8",
            "redirect_uri": "http://localhost:8080/code",
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
