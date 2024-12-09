import logging


class PublishingService:
    def __init__(self, platform_handlers):
        self.handlers = platform_handlers
        logging.info("Publishing service initialized")

    def publish_to_platforms(self, content, selected_platforms):
        logging.info("Starting multi-platform publish")
        success_platforms = []
        failed_platforms = []

        for platform, should_publish in selected_platforms.items():
            logging.debug(f"Publishing to {platform}: {should_publish}")
            print(content[platform])
            if should_publish and platform in content:
                if self.publish_to_platform(platform, content[platform]):
                    success_platforms.append(platform)
                else:
                    failed_platforms.append(platform)

        return success_platforms, failed_platforms

    def publish_to_platform(self, platform, content):
        logging.info(f"Publishing to {platform}")
        handler = self.handlers.get(platform)
        if handler:
            return handler.post(content)
        logging.error(f"No handler found for {platform}")
        return False
