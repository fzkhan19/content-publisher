from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import QTimer
from src.services.ui_service import UIService
from src.services.content_service import ContentService
from src.services.publishing_service import PublishingService
from src.utils.content_generator import ContentGenerator
from src.config.credentials import Credentials
from src.platforms.twitter_handler import TwitterHandler
from src.platforms.linkedin_handler import LinkedInHandler
from src.platforms.bluesky_handler import BlueskyHandler
import sys
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SocialMediaPoster(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_services()
        self.setup_window()
        self.connect_signals()
        self.generated_posts = {}

    def setup_services(self):
        self.credentials = Credentials()
        platform_handlers = {
            "x": TwitterHandler(self.credentials),
            "linkedin": LinkedInHandler(self.credentials),
            "bluesky": BlueskyHandler(self.credentials),
        }

        self.ui_service = UIService(self)
        # Connect model change signal
        self.ui_service.model_selector.currentTextChanged.connect(self.on_model_changed)

        # Create initial content service
        selected_model = self.ui_service.get_selected_model()
        use_ollama = selected_model == "ollama"
        self.content_service = ContentService(ContentGenerator(use_ollama=use_ollama))
        self.publishing_service = PublishingService(platform_handlers)

    def on_model_changed(self, new_model):
        logging.info(f"Model changed to: {new_model.lower()}")
        use_ollama = new_model.lower() == "ollama"
        self.content_service = ContentService(ContentGenerator(use_ollama=use_ollama))

    def setup_window(self):
        self.setWindowTitle("Daily Social Media Poster")
        self.setGeometry(550, 200, 800, 600)

    def connect_signals(self):
        self.ui_service.generate_button.clicked.connect(self.generate_posts)
        self.ui_service.publish_button.clicked.connect(self.publish_posts)
        self.ui_service.model_selector.currentTextChanged.connect(
            self.update_content_service
        )  # New connection

    def connect_signals(self):
        self.ui_service.generate_button.clicked.connect(self.generate_posts)
        self.ui_service.publish_button.clicked.connect(self.publish_posts)

    def generate_posts(self):
        activities = self.ui_service.get_input_text()
        if not activities:
            self.show_message("Error", "Please input your activities for the day.")
            return

        self.ui_service.toggle_loading(True)
        QTimer.singleShot(2000, self.process_generation)

    def process_generation(self):
        activities = self.ui_service.get_input_text()
        self.generated_posts = self.content_service.generate_content(activities)

        if self.generated_posts:
            preview_text = self.content_service.format_preview(self.generated_posts)
            self.ui_service.update_preview(preview_text)
        else:
            self.show_message("Error", "Failed to generate posts. Please try again.")

        self.ui_service.toggle_loading(False)

    def publish_posts(self):
        if not self.generated_posts:
            self.show_message("Error", "Please generate posts first.")
            return

        selected_platforms = self.ui_service.get_selected_platforms()
        if not any(selected_platforms.values()):
            self.show_message(
                "Error", "Please select at least one platform to post to."
            )
            return

        success_platforms, failed_platforms = (
            self.publishing_service.publish_to_platforms(
                self.generated_posts, selected_platforms
            )
        )
        self.show_publish_results(success_platforms, failed_platforms)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def show_publish_results(self, success_platforms, failed_platforms):
        message = ""
        if success_platforms:
            message += f"Successfully posted to: {', '.join(success_platforms)}\n"
        if failed_platforms:
            message += f"Failed to post to: {', '.join(failed_platforms)}"

        title = "Publish Results"
        if failed_platforms and not success_platforms:
            title = "Publishing Failed"
        elif success_platforms and not failed_platforms:
            title = "Publishing Successful"

        self.show_message(title, message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SocialMediaPoster()
    window.show()
    sys.exit(app.exec_())
