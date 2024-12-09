import ollama
import json

class ContentGenerator:
    def __init__(self, model="llama3.2"):
        self.model = model

    def generate_content(self, activities):
        prompts = {
            "x": f"Generate a concise tweet about: {activities}. Include relevant hashtags. Keep it under 280 characters. Return just the tweet text without any explanations.",
            "linkedin": f"Generate a professional LinkedIn post about: {activities}. Include relevant hashtags and maintain professional tone. Keep it under 3000 characters. Return just the post text without any explanations.",
            "bluesky": f"Generate an engaging Bluesky post about: {activities}. Include relevant hashtags. Keep it under 300 characters. Return just the post text without any explanations."
        }

        responses = {}
        for platform, prompt in prompts.items():
            system_prompt = "You are a social media content generator. Respond with only the content requested, no explanations or additional text."
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                system=system_prompt
            )
            responses[platform] = response['response'].strip()

        return json.dumps(responses)