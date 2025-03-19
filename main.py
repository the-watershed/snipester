import sys
import json
import re  # Added import for regular expressions
import requests  # Import requests for making HTTP requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QCheckBox, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import qtawesome as qta
from snipester_utils import paste_clipboard  # Import paste_clipboard
from snipester_stop import on_stop
from snipester_toggle_debug import toggle_debug
from snipester_update_refresh import update_refresh_in_label
from globals import refresh_timer, USE_FALLBACK_SCRAPER
from globals import refresh_in  # Import refresh_in
from link_mod import crop_link  # Import the crop_link function
from link_data import extract_data_from_response  # Import the extract_data_from_response function
from UI import SnipesterUI  # Import the SnipesterUI class
from heartbeat import heartbeat  # Import the heartbeat function

SETTINGS_FILE = "settings.json"

class SnipesterApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = SnipesterUI()  # Instantiate the UI class
        self.setCentralWidget(self.ui)  # Set the central widget to the UI
        self.load_settings()  # Load application settings
        self.ui.refresh_button.clicked.connect(self.on_refresh)  # Connect the refresh button

        # Add labels for pane names
        self.ui.link_label.setText("Link Input Pane")
        self.ui.modified_link_label.setText("Altered Link Pane")
        self.ui.info_label.setText("Information Pane")
        self.ui.debug_label.setText("Debug Pane")

        global refresh_timer
        refresh_timer.timeout.connect(self.update_refresh_in_label)  # Connect update_refresh_in_label
        refresh_timer.start(10)  # Update every 10 milliseconds for hundredths of a second

    def load_settings(self):
        """
        Load application settings from the settings file.
        """
        # Placeholder for loading settings logic
        pass

    def log_debug_info(self, message, data=None):
        """
        Log debug information to the console.
        """
        if data:
            print(f"{message}: {data}")
        else:
            print(message)

    def on_refresh(self):
        """
        Call the heartbeat function to handle refresh logic.
        """
        heartbeat(self)

    def fetch_data_from_link(self, link): 
        print(f"Debug: Fetching data from link: {link}")  # Debugging output

        """
        Fetch data from the provided link and return the response.
        """
        try:
            response = requests.get(link)
            response.raise_for_status()  # Raise an error for bad responses
            print(f"Debug: Raw response content: {response.text}")  # Log the raw response content
            data = response.json()  # Assuming the response is in JSON format
            print(f"Debug: Response data: {data}")  # Debugging output
            return data

        except requests.RequestException as e:
            self.log_debug_info("Error fetching data", str(e))  # Log any errors
            return {}
        except json.JSONDecodeError as e:
            self.log_debug_info("JSON decode error", str(e))  # Log JSON decode errors
            return {}

    def display_info_data(self, data): 
        print(f"Debug: Displaying data: {data}")  # Debugging output

        """
        Display the extracted data in the info_pane with color coding.
        """
        if data:
            # Example of displaying data with color coding
            self.ui.info_pane.setHtml(f"<span style='color: green;'>{data}</span>")  # Display data in green
        else:
            self.ui.info_pane.setPlainText("No data available.")  # Inform the user if no data is available

    def update_refresh_in_label(self):
        """
        Update the refresh timer label with the remaining time.
        """
        global refresh_in  # Declare refresh_in as global
        if refresh_in > 0:
            refresh_in -= 0.01


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SnipesterApp()
    ex.show()
    paste_clipboard(ex.ui)  # Update to use the UI instance
    sys.exit(app.exec_())
