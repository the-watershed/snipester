import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QCheckBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import qtawesome as qta
from http_engine import retrieve_information
from data_extraction import parse_bid_information
from snipester_utils import log_debug_info, is_valid_link, display_info, start_countdown, update_timer, update_info_pane, update_refresh_in_label, paste_clipboard
from snipester_highlight import highlight_all
from snipester_refresh import on_refresh
from snipester_stop import on_stop
from snipester_toggle_debug import toggle_debug
from snipester_update_refresh import update_refresh_in_label
from snipester_auction_ended import auction_ended
from globals import refresh_interval, refresh_timer, refresh_in, timer, no_time_remaining_attempts, retrieval_times

class SnipesterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        global refresh_timer, refresh_in
        refresh_timer.timeout.connect(self.update_refresh_in_label)
        refresh_timer.start(10)  # Update every 10 milliseconds for hundredths of a second

    def initUI(self):
        self.setWindowTitle('Snipester')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.setIcon(qta.icon('fa5s.sync-alt', color='white'))  # Use the correct FontAwesome prefix
        self.refresh_button.setStyleSheet("background-color: #3498DB; color: #ECF0F1;")
        self.refresh_button.setFixedWidth(100)  # Set button width
        self.refresh_button.clicked.connect(self.on_refresh)
        button_layout.addWidget(self.refresh_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.setIcon(qta.icon('fa5s.stop', color='white'))  # Use the correct FontAwesome prefix
        self.stop_button.setStyleSheet("background-color: #E74C3C; color: #ECF0F1;")
        self.stop_button.setFixedWidth(100)  # Set button width
        self.stop_button.clicked.connect(self.on_stop)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

        link_layout = QVBoxLayout()
        link_label = QLabel('Enter link here:', self)
        link_label.setStyleSheet("color: #FFFFFF; background-color: #1C2833; font-weight: bold;")
        link_layout.addWidget(link_label)
        self.link_input = QTextEdit(self)
        self.link_input.setStyleSheet("background-color: #2C3E50; color: #ECF0F1;")
        self.link_input.setFixedHeight(75)  # Make the input box 3 lines tall
        self.link_input.setAcceptRichText(False)  # Disable rich text to prevent HTML conversion
        self.link_input.mousePressEvent = self.highlight_all  # Connect mouse press event to highlight_all
        self.link_input.keyPressEvent = self.handle_key_press  # Connect key press event to handle_key_press
        link_layout.addWidget(self.link_input)

        modified_link_label = QLabel('Altered HTML link:', self)
        modified_link_label.setStyleSheet("color: #FFFFFF; background-color: #1C2833; font-weight: bold;")
        link_layout.addWidget(modified_link_label)
        self.modified_link_pane = QTextEdit(self)
        self.modified_link_pane.setReadOnly(True)
        self.modified_link_pane.setStyleSheet("background-color: #34495E; color: #ECF0F1;")
        self.modified_link_pane.setFixedHeight(75)  # Make the input box 3 lines tall
        self.modified_link_pane.setFont(QFont("Arial", 12))  # Set a more readable font
        link_layout.addWidget(self.modified_link_pane)

        main_layout.addLayout(link_layout)

        self.debug_checkbox = QCheckBox('Debug', self)
        self.debug_checkbox.setStyleSheet("color: #ECF0F1;")
        self.debug_checkbox.stateChanged.connect(self.toggle_debug)
        main_layout.addWidget(self.debug_checkbox)

        self.info_pane = QTextEdit(self)
        self.info_pane.setReadOnly(True)
        self.info_pane.setStyleSheet("background-color: #34495E; color: #ECF0F1;")
        self.info_pane.setFont(QFont("Arial", 12))  # Set a more readable font
        main_layout.addWidget(self.info_pane)

        self.debug_pane = QTextEdit(self)
        self.debug_pane.setReadOnly(True)
        self.debug_pane.setStyleSheet("background-color: #34495E; color: #ECF0F1;")
        self.debug_pane.hide()
        main_layout.addWidget(self.debug_pane)

        self.end_date_label = QLabel(self)
        self.end_date_label.setStyleSheet("color: #ECF0F1;")
        main_layout.addWidget(self.end_date_label)

        self.refresh_in_label = QLabel(self)
        self.refresh_in_label.setStyleSheet("color: #ECF0F1;")
        main_layout.addWidget(self.refresh_in_label)

        self.setLayout(main_layout)

    def highlight_all(self, event):
        highlight_all(self, event)

    def handle_key_press(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.update_modified_link_pane()
        else:
            QTextEdit.keyPressEvent(self.link_input, event)

    def on_refresh(self):
        on_refresh(self)

    def on_stop(self):
        on_stop(self)

    def toggle_debug(self, state):
        toggle_debug(self, state)

    def update_refresh_in_label(self):
        update_refresh_in_label(self)

    def auction_ended(self):
        auction_ended(self)

    def calculate_refresh_interval(self, time_remaining):
        total_seconds = 0
        days_match = re.search(r'(\d+)d', time_remaining)
        hours_match = re.search(r'(\d+)h', time_remaining)
        minutes_match = re.search(r'(\d+)m', time_remaining)
        seconds_match = re.search(r'(\d+)s', time_remaining)

        if days_match:
            total_seconds += int(days_match.group(1)) * 86400  # 24 hours * 3600 seconds
        if hours_match:
            total_seconds += int(hours_match.group(1)) * 3600
        if minutes_match:
            total_seconds += int(minutes_match.group(1)) * 60
        if seconds_match:
            total_seconds += int(seconds_match.group(1))

        return total_seconds

    def strip_html_link(self, link):
        match = re.search(r'(https://www\.ebay\.com/itm/\d+)', link)
        if match:
            return match.group(1)
        return link

    def update_modified_link_pane(self):
        link = self.link_input.toPlainText()
        modified_link = self.strip_html_link(link)
        self.modified_link_pane.setText(modified_link)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SnipesterApp()
    ex.show()
    paste_clipboard(ex)  # Paste clipboard content into the link input on startup
    sys.exit(app.exec_())
