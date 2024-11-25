from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QCheckBox, QLabel, QWidget,
    QStackedLayout, QProgressBar
)
from PyQt5.QtCore import Qt
import logging

class UIService:
    def __init__(self, main_widget):
        self.widget = main_widget
        self.setup_ui_components()
        logging.info("UI Service initialized")

    def setup_ui_components(self):
        self.main_layout = QVBoxLayout(self.widget)
        self.stacked_layout = QStackedLayout()
        self.main_widget = QWidget()
        self.loading_overlay = self.create_loading_overlay()

        self.build_main_layout()

        self.stacked_layout.addWidget(self.main_widget)
        self.stacked_layout.addWidget(self.loading_overlay)
        self.main_layout.addLayout(self.stacked_layout)
        self.stacked_layout.setCurrentWidget(self.main_widget)

    def create_loading_overlay(self):
        overlay = QWidget(self.widget)
        overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.7);
            }
            QLabel {
                color: #333;
                font-size: 18px;
                font-weight: bold;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
        """)

        layout = QVBoxLayout(overlay)

        spinner = QProgressBar()
        spinner.setMinimum(0)
        spinner.setMaximum(0)
        spinner.setFixedSize(100, 20)

        loading_label = QLabel("Generating content...")
        loading_label.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(spinner, 0, Qt.AlignCenter)
        layout.addWidget(loading_label, 0, Qt.AlignCenter)
        layout.addStretch()

        return overlay

    def build_main_layout(self):
        layout = QVBoxLayout(self.main_widget)

        # Input section
        self.input_area = self.create_input_section(layout)

        # Platform selection
        self.platform_checkboxes = self.create_platform_section(layout)

        # Generate button
        self.generate_button = QPushButton("Generate Posts")
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        layout.addWidget(self.generate_button)

        # Preview section
        self.preview_area = self.create_preview_section(layout)

        # Publish button
        self.publish_button = QPushButton("Publish Posts")
        self.publish_button.setStyleSheet("background-color: #008CBA; color: white; padding: 5px;")
        layout.addWidget(self.publish_button)

    def create_input_section(self, parent_layout):
        input_section = QVBoxLayout()
        input_label = QLabel("What cool things did you do today?")
        input_area = QTextEdit()
        input_area.setMinimumHeight(100)
        input_section.addWidget(input_label)
        input_section.addWidget(input_area)
        parent_layout.addLayout(input_section)
        return input_area

    def create_platform_section(self, parent_layout):
        platform_section = QVBoxLayout()
        platform_label = QLabel("Select platforms to post:")
        platform_section.addWidget(platform_label)

        checkboxes = {
            "x": QCheckBox("Post on X"),
            "linkedin": QCheckBox("Post on LinkedIn"),
            "bluesky": QCheckBox("Post on Bluesky")
        }

        checkbox_layout = QHBoxLayout()
        for checkbox in checkboxes.values():
            checkbox_layout.addWidget(checkbox)
        platform_section.addLayout(checkbox_layout)
        parent_layout.addLayout(platform_section)
        return checkboxes

    def create_preview_section(self, parent_layout):
        preview_section = QVBoxLayout()
        preview_label = QLabel("Generated Posts Preview:")
        preview_area = QTextEdit()
        preview_area.setReadOnly(True)
        preview_area.setMinimumHeight(200)
        preview_section.addWidget(preview_label)
        preview_section.addWidget(preview_area)
        parent_layout.addLayout(preview_section)
        return preview_area

    def toggle_loading(self, show):
        self.stacked_layout.setCurrentWidget(self.loading_overlay if show else self.main_widget)

    def update_preview(self, preview_text):
        self.preview_area.setText(preview_text)

    def get_input_text(self):
        return self.input_area.toPlainText().strip()

    def get_selected_platforms(self):
        return {
            platform: checkbox.isChecked()
            for platform, checkbox in self.platform_checkboxes.items()
        }
