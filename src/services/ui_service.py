from qfluentwidgets import (
    CheckBox,
    TextEdit,
    ProgressBar,
    PrimaryPushButton,
    StrongBodyLabel,
    BodyLabel,
    FluentWindow,
    FluentIcon,
    InfoBar,
)
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QStackedLayout
from PyQt5.QtCore import Qt
import logging


class UIService:
    def __init__(self, main_widget):
        self.widget = main_widget
        self.setup_ui_components()
        self.setup_button_style()
        logging.info("UI Service initialized")

    def setup_button_style(self):
        button_style = """
            PrimaryPushButton {
                background-color: black;
                color: #fafafa;
                border: 1px solid white;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            PrimaryPushButton:hover {
                background-color: #18181a;
            }
        """
        self.generate_button.setStyleSheet(button_style)
        self.publish_button.setStyleSheet(button_style)

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
        layout = QVBoxLayout(overlay)

        spinner = ProgressBar()
        spinner.setMinimum(0)
        spinner.setMaximum(0)
        spinner.setFixedSize(200, 4)

        loading_label = BodyLabel("Generating content...")
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
        self.generate_button = PrimaryPushButton("Generate Posts")
        layout.addWidget(self.generate_button)

        # Preview section
        self.preview_area = self.create_preview_section(layout)

        # Publish button
        self.publish_button = PrimaryPushButton("Publish Posts")
        layout.addWidget(self.publish_button)

    def create_input_section(self, parent_layout):
        input_section = QVBoxLayout()
        input_label = StrongBodyLabel("What cool things did you do today?")
        input_area = TextEdit()
        input_area.setMinimumHeight(100)
        input_section.addWidget(input_label)
        input_section.addWidget(input_area)
        parent_layout.addLayout(input_section)
        return input_area

    def create_platform_section(self, parent_layout):
        platform_section = QVBoxLayout()
        platform_label = StrongBodyLabel("Select platforms to post:")
        platform_section.addWidget(platform_label)

        checkboxes = {
            "x": CheckBox("Post on X"),
            "linkedin": CheckBox("Post on LinkedIn"),
            "bluesky": CheckBox("Post on Bluesky"),
        }

        checkbox_layout = QHBoxLayout()
        for checkbox in checkboxes.values():
            checkbox_layout.addWidget(checkbox)
        platform_section.addLayout(checkbox_layout)
        parent_layout.addLayout(platform_section)
        return checkboxes

    def create_preview_section(self, parent_layout):
        preview_section = QVBoxLayout()
        preview_label = StrongBodyLabel("Generated Posts Preview:")
        preview_area = TextEdit()
        preview_area.setReadOnly(True)
        preview_area.setMinimumHeight(200)
        preview_section.addWidget(preview_label)
        preview_section.addWidget(preview_area)
        parent_layout.addLayout(preview_section)
        return preview_area

    def toggle_loading(self, show):
        self.stacked_layout.setCurrentWidget(
            self.loading_overlay if show else self.main_widget
        )

    def update_preview(self, preview_text):
        self.preview_area.setText(preview_text)

    def get_input_text(self):
        return self.input_area.toPlainText().strip()

    def get_selected_platforms(self):
        return {
            platform: checkbox.isChecked()
            for platform, checkbox in self.platform_checkboxes.items()
        }
