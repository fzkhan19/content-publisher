import google.generativeai as genai
import json
import os
import ollama


class ContentGenerator:

    def __init__(self, model="gemini-pro", use_ollama=False):
        if use_ollama:
            self.model = "llama3.2"
        else:
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.model = genai.GenerativeModel(model)

    def generate_content(self, activities):
        prompts = {
            "x": f"Generate a concise tweet about: {activities}. Include relevant hashtags. Keep it under 280 characters. Return just the tweet text without any explanations.",
            "linkedin": f"Generate a professional LinkedIn post about: {activities}. Include relevant hashtags and maintain professional tone. Keep it under 2500 characters. Return just the post text without any explanations.",
            "bluesky": f"Generate an engaging Bluesky post about: {activities}. Include relevant hashtags. Keep it under 280 characters. Return just the post text without any explanations.",
        }

        responses = {}
        for platform, prompt in prompts.items():
            if self.model == "llama3.2":
                system_prompt = "You are a social media content generator. Respond with only the content requested, no explanations or additional text."
                response = ollama.generate(
                    model=self.model, prompt=prompt, system=system_prompt
                )
                responses[platform] = response["response"].strip()
            else:
                response = self.model.generate_content(
                    contents=[{"role": "user", "parts": [prompt]}],
                    generation_config={
                        "temperature": 0.9,  # Increased for more creative/natural output
                        "top_p": 0.9,
                        "top_k": 40,
                    },
                )
                responses[platform] = response.text.strip()

        return json.dumps(responses)
