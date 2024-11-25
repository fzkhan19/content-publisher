import logging
import json

class ContentService:
    def __init__(self, content_generator):
        self.content_generator = content_generator
        logging.info("Content service initialized")

    def generate_content(self, activities):
        logging.info("Starting content generation")
        if not activities:
            logging.warning("No activities provided")
            return None

        logging.debug(f"Activities received: {activities}")
        json_response = self.content_generator.generate_content(activities)
        generated_posts = json.loads(json_response)

        if generated_posts:
            logging.info("Successfully generated posts")
            return generated_posts

        logging.error("Failed to generate posts")
        return None

    def format_preview(self, generated_posts):
        preview_text = ""
        for platform, content in generated_posts.items():
            preview_text += f"=== {platform} ===\n{content}\n\n"
        return preview_text
